import duckdb

def execute_query(tables: dict, sql: str):
    con = duckdb.connect()

    for name, df in tables.items():
        con.register(name, df)

    return con.execute(sql).fetchdf()