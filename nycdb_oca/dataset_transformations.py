from nycdb.dataset_transformations import to_csv


def oca(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    return _to_csv