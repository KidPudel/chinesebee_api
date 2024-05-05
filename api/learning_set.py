from database.chinesebee_db import db_conn
from utils.results import error_result


def save_word(user_id: int, word_id: int):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "insert into saved_words(user_id, word_id) values(%(user)s, %(word)s)",
            {"user": user_id, "word": word_id},
        )
        db_conn.commit()

        if cursor.rowcount == 0:
            return error_result(err_msg="failed to insert word")
        return {
            "success": True,
        }
