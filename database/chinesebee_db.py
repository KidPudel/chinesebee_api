import psycopg
from psycopg.rows import dict_row
from psycopg import Connection
import os

PGURL = os.environ.get("DATABASE_URL")

db_conn: Connection = psycopg.connect(
    PGURL,
    row_factory=dict_row,
)
