import pandas as pd
from database.connector import get_connection


def execute_query(query):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    cursor.close()
    connection.close()

    dataframe = pd.DataFrame(rows, columns=columns)

    return dataframe