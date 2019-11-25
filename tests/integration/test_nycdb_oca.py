import psycopg2
import psycopg2.extras
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from types import SimpleNamespace
from decimal import Decimal
import subprocess
import sys
import pytest
import dotenv

import nycdb

dotenv.load_dotenv()

my_dir = os.path.dirname(__file__)

data_dir = os.path.join(my_dir, 'data')

ARGS = SimpleNamespace(
    user=os.environ.get('NYCDB_TEST_POSTGRES_USER', ''),
    password=os.environ.get('NYCDB_TEST_POSTGRES_PASSWORD', ''),
    host=os.environ.get('NYCDB_TEST_POSTGRES_HOST', ''),
    database=os.environ.get('NYCDB_TEST_POSTGRES_DB', ''),
    port=os.environ.get('NYCDB_TEST_POSTGRES_PORT', ''),
    root_dir=data_dir
)

CONNECT_ARGS = dict(
    user=ARGS.user,
    password=ARGS.password,
    host=ARGS.host,
    database=ARGS.database,
    port=ARGS.port
)


def create_db(dbname):
    args = CONNECT_ARGS.copy()
    del args['database']
    conn = psycopg2.connect(**args)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as curs:
        curs.execute('CREATE DATABASE ' + dbname)
    conn.close()


@pytest.fixture(scope="session")
def db():
    """
    Attempt to connect to the database, retrying if necessary, and also
    creating the database if it doesn't already exist.
    """

    retries_left = 5

    while True:
        try:
            psycopg2.connect(**CONNECT_ARGS).close()
            return
        except psycopg2.OperationalError as e:
            if 'database "{}" does not exist'.format(ARGS.database) in str(e):
                create_db(ARGS.database)
                retries_left -= 1
            elif retries_left:
                # It's possible the database is still starting up.
                time.sleep(2)
                retries_left -= 1
            else:
                raise e


@pytest.fixture
def conn(db):
    with psycopg2.connect(**CONNECT_ARGS) as conn:
        yield conn


def drop_table(conn, table_name):
    with conn.cursor() as curs:
        curs.execute('DROP TABLE IF EXISTS {};'.format(table_name))
    conn.commit()


def row_count(conn, table_name):
    with conn:
        with conn.cursor() as curs:
            curs.execute('select count(*) from {}'.format(table_name))
            return curs.fetchone()[0]


def has_one_row(conn, query):
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            return bool(curs.fetchone())


def table_columns(conn, table_name):
    sql = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(
        table_name)
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            return [x[0] for x in curs.fetchall()]

# NOTE: This test has to be updated each time the test data is rebuilt
def test_oca(conn):
    drop_table(conn, 'oca_index')
    drop_table(conn, 'oca_causes')
    drop_table(conn, 'oca_addresses')
    drop_table(conn, 'oca_parties')
    drop_table(conn, 'oca_events')
    drop_table(conn, 'oca_appearances')
    drop_table(conn, 'oca_appearance_outcomes')
    drop_table(conn, 'oca_motions')
    drop_table(conn, 'oca_decisions')
    drop_table(conn, 'oca_judgments')
    drop_table(conn, 'oca_warrants')
    oca = nycdb.Dataset('oca', args=ARGS)
    oca.db_import()
    assert row_count(conn, 'oca_index') == 50
    assert row_count(conn, 'oca_causes') == 50
    assert row_count(conn, 'oca_addresses') == 50
    assert row_count(conn, 'oca_parties') == 122
    assert row_count(conn, 'oca_events') == 89
    assert row_count(conn, 'oca_appearances') == 123
    assert row_count(conn, 'oca_appearance_outcomes') == 106
    assert row_count(conn, 'oca_motions') == 39
    assert row_count(conn, 'oca_decisions') == 24
    assert row_count(conn, 'oca_judgments') == 23
    assert row_count(conn, 'oca_warrants') == 23
    case = '00000414FEEFDB09FADC092CBA4A47C2D997FDE65E31F18F3A40F0BF4060BDAD'
    assert has_one_row(conn, f"select * from oca_index where indexnumberid = '{case}'")
