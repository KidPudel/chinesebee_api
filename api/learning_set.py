from database.chinesebee_db import db_conn
from utils.results import error_result
from utils.decorators import tireless_connection


@tireless_connection
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


@tireless_connection
def get_saved_words(user_id: int):
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            select
                saved.id saved_id,
                hsk.id word_id,
                hsk.chinese,
                hsk.pinyin,
                hsk.english,
                hsk.russian,
                hsk.hsk_level
            from
                hsk_words hsk
                inner join saved_words saved on hsk.id = saved.word_id
            where
                saved.user_id = %s
            """,
            (user_id,),
        )
        users_saved_words = cursor.fetchall()
        if users_saved_words == None:
            return error_result(err_msg="failed to find saved words for the user")
        return {
            "success": True,
            "saved_words": users_saved_words
        }
        

@tireless_connection
def delete_saved_word(saved_id: int):
    with db_conn.cursor() as cursor:
        cursor.execute("delete from saved_words where id = %s", (saved_id,))
        db_conn.commit()
        if cursor.rowcount == 0:
            return error_result(err_msg="didn't delete")
        return {
            "success": True
        }


@tireless_connection
def check_can_train(user_id: int):
    with db_conn.cursor() as cursor:
        cursor.execute("select id from saved_words where user_id = %s", (user_id,))
        word_number = len(cursor.fetchall())
        if word_number < 5:
            return {
                "success": True,
                "can_learn": False,
                "msg": f"Не хватает {5 - word_number} слов"
            }
        else:
            return {
                "success": True,
                "can_learn": True
            }