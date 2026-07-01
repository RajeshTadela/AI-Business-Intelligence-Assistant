import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    return connection

def test_connection():
    connection = get_connection()

    if connection.is_connected():
        print("✅ Successfully connected to MySQL!")
        connection.close()
        print("Connection closed")
        
    else:
        print("❌ Connection failed.")

if __name__ == "__main__":
    test_connection()