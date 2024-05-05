import psycopg
from psycopg.rows import dict_row

db_conn = psycopg.connect("dbname=chinesebee_db user=postgres", row_factory=dict_row)