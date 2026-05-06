import pandas as pd

def infer_schema_from_multiple(files):
    tables = {}
    schema_blocks = []

    for file in files:
        table_name = file.name.split(".")[0].replace(" ", "_")

        # ✅ Keep your fix
        df = pd.read_csv(file, on_bad_lines='skip')

        # ✅ NEW: auto type handling
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

        tables[table_name] = df

        cols = []
        for col, dtype in zip(df.columns, df.dtypes):
            sql_type = map_dtype(col, dtype)
            cols.append(f"    {col} {sql_type}")

        schema_blocks.append(
            f"Table: {table_name}\nColumns:\n" + "\n".join(cols)
        )

    return "\n\n".join(schema_blocks), tables


def map_dtype(col, dtype):
    dtype = str(dtype)

    if "date" in col.lower():
        return "DATE"
    elif "int" in dtype:
        return "INT"
    elif "float" in dtype:
        return "FLOAT"
    elif "bool" in dtype:
        return "BOOLEAN"
    else:
        return "VARCHAR"