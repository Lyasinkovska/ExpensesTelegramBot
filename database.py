import sqlite3

connection = sqlite3.connect("finance.db", check_same_thread=False)
cursor = connection.cursor()


def insert(table: str, column_values: dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f'INSERT INTO {table}'
        f'({columns}) '
        f'VALUES ({placeholders})',
        values)
    connection.commit()


def fetchall(table: str, *columns: str) -> dict:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = {}
    for i in range(len(columns)):
        result.update({str(values[0]): {columns[i]: values[i]} for values in rows})
    return result


# def delete(table: str, row_id: int) -> None:
#     row_id = int(row_id)
#     cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
#     connection.commit()


def get_cursor():
    return cursor


def _init_db():
    """Initialize DataBase"""
    with open("create_db.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    connection.commit()


def check_db_exists():
    """Check id Database exists, otherwise creates DB"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='Expenses'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
