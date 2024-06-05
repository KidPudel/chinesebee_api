import psycopg
from psycopg.rows import dict_row
import os

PGURL = "postgresql://postgres:iMyWAfNNjHlWQUMevbgZXLASzsOwojod@monorail.proxy.rlwy.net:47948/railway"

db_conn = psycopg.connect(
    PGURL,
    row_factory=dict_row,
)
