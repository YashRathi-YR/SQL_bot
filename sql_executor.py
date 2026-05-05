import duckdb

def execute_query(df, sql):
    con = duckdb.connect()
    con.register("uploaded_table", df)

    result = con.execute(sql).fetchdf()
    return result