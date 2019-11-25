import os
import psycopg2

DB_URL = 'postgres://maxwell:@localhost/nycdb'

OCA_TABLES = [
    'oca_index',
    'oca_causes',
    'oca_addresses',
    'oca_parties',
    'oca_events',
    'oca_appearances',
    'oca_appearance_outcomes',
    'oca_motions',
    'oca_decisions',
    'oca_judgments',
    'oca_warrants',
]

# 50 cases
CASES = [
    '00000414FEEFDB09FADC092CBA4A47C2D997FDE65E31F18F3A40F0BF4060BDAD',
    '00003AC2883F5605743DA33441D59667FFD553E24D76E61440D969B1424B12C3',
    '00016CC04DBD0E381382BCBD2A8F42DEA456F395C9AA120B1B8D5CA8226A1457',
    '0002E0F92F3D6E9A9BA9A2B740D183A31828C6109C84D57B5F19F58B985D9B67',
    '0002F0BABAE75F6A2CF7A5F3C3782BA81BE561167D5863077BCE15555BF94B74',
    '00030745CEA60D09B6BFD349FBB5EF2EC075B48884EB0C8C25F23A01B6B5D001',
    '000391F899DE0F103A3C5EEEF2596758419D425F9071FC4CE9E2B2F619949B45',
    '0003BD7AF98F85622FE51FB7463BCE29F16A8254E1F68DC745FE5671D3B09419',
    '0003F3C66EE9083D58500DFBB504F52A6D5A980874C93AA30944ECEAC305B03C',
    '0004758245508457E02D51552D0157B4A6ED5827ED32A34F484F602803A06C18',
    '00048F7A7FB3F7F41C50701FB015CD2A74F6C84BF53BC19105F453B26A155BC4',
    '0004F1C81F634021AB18F8A2218EE720A5D99025923699D62BC7B09E6899A709',
    '0005032564B7ADCBEDC5259A8947E7BECC2872CABB228F0B005EEFB9BD704646',
    '0005C9915E10C68068D0D5195FA7A6A5AB185F82F0F7266CB5388F4F130FC96A',
    '0006307754C317AE94150FB0D61CE641D1A39849035F2366B133CAE3AA017C48',
    '00064A2A644327B003D0E184A3EC2E3C59CED7B095670949D3CF54234E178CE2',
    '00069708EB17C1D9E50E5AD5764CABE2E9335F4EE19E8BB00EA9E18E06735258',
    '0006C952B63779F0A6387CE123EA53930B372B61A5A4AD6E752191B92CF46634',
    '0006EE4BAEE8F2C2486799AEC1937C2F411B9FB6050EAD59D734E3FAEB65882E',
    '00072178A23C8A542467CD8055EFA813049D9D0E4C19B989000E57B15F7490C4',
    '0007303561978630F82D941F212CFD19A03EBE78C871DD51D25F5BF03E10FD23',
    '000742ABF556258617E2FF6F5BC505561BFF7011373BA99624BE7CEA1ECDC92B',
    '0007A4C3D315FF6B1E1AD03A631155F669C077885DA25B62C3248EAF6C811D40',
    '0007B1E350D51DAFD2CE346BABF403074D29A988CF0B6B70C0B6190576B9031B',
    '0007C8AD40B56E3C282A60ADDDD51F796956B596EB5818E14D22FDE1BC9AB676',
    '0007CA08D63A65E2D2A4C032C8013EE464CEA4A8001AED65481BB975E5274392',
    '0007E13D3F577571E0A8BA9B9CA2050E9B42EE82E56A33D12DE8F5018E451163',
    '0007EA2D2E2C97208E5CD8513402D82376560A8F74EE0D5C9D61012FC1A39B65',
    '0008127E639B0D635DA5A2550ED09AA44A152BDDC767546750EF00B98A63CD4A',
    '0008311573264CC6795F9A8B297528946B7FABBF2B97DB701F706309943BD7A0',
    '00085E126F7AF158D6EE56E07CBBF58655A3320486EAB841EE191E80F8BE5DFC',
    '00085E5AD2AE104AB3D88241C567A87C610368C2DB53E2CC42468767CF849A84',
    '0008690F97438E6FC18A27D8A52DA40E910E9620F80C825244037CA778B6B7C1',
    '000996F37436E347BE03DF58C7450CBB4C2AF462458A1F020DF71BCF2033F093',
    '0009B4C72E825A195484D942B3A48E7B9380B5A6BB2B5DB81D2EEA7408B97A6F',
    '000A69A6535001E7832255BDA3BE2171F27878253A96FC9755268D533EF31890',
    '000AF5DB052606425D3E6918FF179BB7A0FB3677FCFB4356F6E14322D045E495',
    '000B2C3362889523D3794CF15B32DA5EB924ADD3925B8D7928218033CB05CB9B',
    '000B9755A6C573E4759315A5BE7C40DC6B27CF7CA81CC6AB4EA2C223378596BD',
    '000BA850EC6943231AF119EA36ADC6991F6206E93CFCE21442EB44C9AC68B981',
    '000BCF2708FDDD3D697FCC85775D3FF2B371B5D13837F34CBF9BDD4CDCE7BDF5',
    '000BE818B0FE7A4F0E6EBBB1341EAE6EA5C4A8DB285817FBC3F609E8DC11F0A2',
    '000BF833386F5D7BAF048B5AF1B1781188784097124D7A05270A91C52F4D5AFD',
    '000C083D6F510F8F8F57704207F6D90A1C2ED5060728C5795837F69EAEB2079D',
    '000C1088CCEC96636E8489B3338EE07E74CEACE53EE29C3410C2D0F4C1AC992E',
    '000C2C65ACBC4B58C7E9C843B34D6167A9AAE7DAE68A50D0480B332C82795083',
    '000C3193BE5A56EBFCA5E032D7CEF044D1CF56AD682BD5BD3425792ABC39B63D',
    '000CA90E03F0BFC3643D3F533CD9526016CF32482D5764613661EC19EF59EA41',
    '000EC85692EDAC4F0EC87B25B4B9DF2FD3CE618286B825B1015B20A4DFFBC6FE',
    '000EFE09F1F308DB90B220BAAF8E00767C43DD149DF4E524D2E9CB847618D795',
]


def export_query_csv(conn, query, file_path):

    f = open(file_path, 'w')

    with conn.cursor() as curs:
        curs.copy_expert(f"COPY ({query}) TO STDOUT WITH CSV HEADER ", f)

    f.close()

def export_cases_csv(conn, table_name, cases, file_path):
    cases = ','.join(["'" + i + "'" for i in cases])
    query = f"SELECT * FROM {table_name} WHERE indexnumberid IN ({cases})"
    export_query_csv(conn, query, file_path)



con = psycopg2.connect(DB_URL)

for t in OCA_TABLES:
    file_path = os.path.join(os.path.dirname(__file__), 'tests', 'integration', 'data', f"{t}.csv")

    export_cases_csv(con, t, CASES, file_path)