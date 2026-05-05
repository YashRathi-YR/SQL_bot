import pandas as pd

def infer_schema_from_csv(file):
    df = pd.read_csv(file, on_bad_lines='skip')

    table_name = "uploaded_table"
    schema_lines = []

    for col, dtype in zip(df.columns, df.dtypes):
        sql_type = map_dtype(dtype)
        schema_lines.append(f"    {col} {sql_type}")

    schema = f"Table: {table_name}\nColumns:\n" + "\n".join(schema_lines)

    return schema, df


def map_dtype(dtype):
    dtype = str(dtype)

    if "int" in dtype:
        return "INT"
    elif "float" in dtype:
        return "FLOAT"
    elif "object" in dtype:
        return "VARCHAR"
    elif "bool" in dtype:
        return "BOOLEAN"
    else:
        return "VARCHAR"