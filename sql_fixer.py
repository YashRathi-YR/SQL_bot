def fix_sql(sql: str, error: str) -> str:
    # Fix date_part / AVG on VARCHAR
    if "VARCHAR" in error and "date" in error.lower():
        sql = sql.replace("order_date", "CAST(order_date AS DATE)")

    return sql