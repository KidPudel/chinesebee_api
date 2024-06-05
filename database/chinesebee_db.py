import psycopg
from psycopg.rows import dict_row
import os

PGURL = os.environ.get("DATABASE_URL")

db_conn = psycopg.connect(
    PGURL,
    row_factory=dict_row,
)
