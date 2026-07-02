from pathlib import Path
import pandas as pd
from database.connector import get_connection


def get_csv_files(folder_path):
    """Return all CSV files inside a folder."""
    folder = Path(folder_path)
    return list(folder.glob("*.csv"))


def read_csv(file_path):
    """Read a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def infer_mysql_type(dtype):
    """Convert Pandas data types to MySQL data types."""

    dtype = str(dtype)

    if "int" in dtype:
        return "INT"

    elif "float" in dtype:
        return "DOUBLE"

    elif "datetime" in dtype:
        return "DATETIME"

    elif "bool" in dtype:
        return "BOOLEAN"

    else:
        return "VARCHAR(255)"


def create_table(cursor, table_name, dataframe):
    """Create a MySQL table based on DataFrame columns."""

    columns = []

    for column_name, dtype in dataframe.dtypes.items():
        mysql_type = infer_mysql_type(dtype)
        columns.append(f"`{column_name}` {mysql_type}")

    column_query = ", ".join(columns)

    query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        {column_query}
    );
    """

    cursor.execute(query)


def insert_data(cursor, table_name, dataframe):
    """Insert DataFrame rows into MySQL."""

    # Convert NaN to None (SQL NULL)
    dataframe = dataframe.where(pd.notnull(dataframe), None)

    columns = ", ".join([f"`{col}`" for col in dataframe.columns])

    placeholders = ", ".join(["%s"] * len(dataframe.columns))

    query = f"""
    INSERT INTO `{table_name}`
    ({columns})
    VALUES ({placeholders})
    """

    data = [tuple(row) for row in dataframe.itertuples(index=False)]

    cursor.executemany(query, data)

def import_folder(folder_path):

    connection = get_connection()

    cursor = connection.cursor()

    files = get_csv_files(folder_path)

    for file in files:

        print(f"Importing {file.name}...")

        dataframe = read_csv(file)

        table_name = file.stem.replace("-", "_").lower()

        create_table(cursor, table_name, dataframe)

        insert_data(cursor, table_name, dataframe)

        print(f"✓ {table_name} imported.")

    connection.commit()

    cursor.close()

    connection.close()

    print("\n🎉 Import Completed Successfully!")

if __name__ == "__main__":
    import_folder("datasets/Awesome Chocolates")