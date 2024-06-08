from database.chinesebee_db import db_conn
from psycopg import connect
import os


def tireless_connection(lazy_connector):
    def wrapper(*args, **kwargs):
        global db_conn
        if db_conn.closed:
            db_conn = connect(os.environ.get("DATABASE_URL"))
        return lazy_connector(*args, **kwargs)
    return wrapper
