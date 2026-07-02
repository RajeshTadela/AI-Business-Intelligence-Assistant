from database.connector import get_connection


def get_tables():
    """
    Returns a list of all tables in the connected database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = DATABASE();
    """

    cursor.execute(query)

    tables = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return tables


def get_columns(table_name):
    """
    Returns all columns of a given table.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = %s;
    """

    cursor.execute(query, (table_name,))

    columns = cursor.fetchall()

    cursor.close()
    connection.close()

    return columns


def get_schema():
    """
    Returns the complete schema of the connected database.
    """

    schema = {}

    tables = get_tables()

    for table in tables:
        schema[table] = get_columns(table)

    return schema