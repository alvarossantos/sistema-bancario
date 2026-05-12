import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class BancoDeDados:
    def __init__(self):
        self.config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }

    def __enter__(self):
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    teste = BancoDeDados()
    print("Conectado? ", teste)
