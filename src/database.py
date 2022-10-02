import os

import psycopg2


def connect_to_db():
    db_name = os.environ.get("POSTGRES_DATABASE")
    db_host = os.environ.get("POSTGRES_HOST")
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_port = os.environ.get("POSTGRES_PORT")
    connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port,
    )
    return connection


def close_db_connection(connection):
    connection.close()
