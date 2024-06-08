from database.chinesebee_db import db_conn
from utils.results import error_result
from utils.decorators import tireless_connection


@tireless_connection
def get_chinese_match(word: str):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "select id, chinese, russian from hsk_words where lower(russian) like lower(%s) order by CHAR_LENGTH(russian) asc",
            ("%" + word.lower() + "%",),
        )
        match = cursor.fetchall()
        if match == None:
            return error_result(err_msg="word not found")
        return {"success": True, "match": match}


@tireless_connection
def get_word_details(id: int):
    with db_conn.cursor() as cursor:
        cursor.execute("select chinese, pinyin, english, russian, hsk_level from hsk_words where id = %s", (id,))
        details = cursor.fetchone()
        if details == None:
            return error_result(err_msg="no word found")
        return {
            "success": True,
            "details": details
        }
