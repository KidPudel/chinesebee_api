from fastapi import FastAPI, Path, Form, Query, Request, Response
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

from api.chinese_search import get_chinese_match, get_word_details
from api.learning_set import save_word, get_saved_words, delete_saved_word, check_can_train
from api.image_recognition import score_accuracy
from utils.results import error_result


app = FastAPI()


# preflight for accuracy-score
@app.options("/accuracy-score")
async def preflight_handler():
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = "https://chinese-bee-dictation-production.up.railway.app"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    return response

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "https://chinese-bee-dictation-production.up.railway.app"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chinese-bee-dictation-production.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "alive"}


@app.get("/chinese-match/{word}")
def chinese_match(
    word: Annotated[str, Path(description="word for which to find chinese word")]
):
    if word == "":
        return error_result(err_msg="no word provided")
    print("got word")
    return get_chinese_match(word=word)


@app.get("/word-details/{id}")
def word_details_handler(id: Annotated[int | None, Path(description="id")]):
    if id == None or id < 0:
        return error_result(err_msg="no id provided or id is incorrect")
    return get_word_details(id=id)


@app.post("/new-word", description="insert a new word to the learning set")
def new_word_handler(
    user_id: Annotated[int | None, Form(description="user to save to")] = None,
    word_id: Annotated[int | None, Form(description="word id to save")] = None,
):
    if user_id == None or user_id < 0:
        return error_result(err_msg="no user id or id is incorrect")
    if word_id == None or word_id < 0:
        return error_result(err_msg="no word id provided or id is incorrect")

    return save_word(user_id=user_id, word_id=word_id)


@app.get("/saved-words", description="get learning set associated with the user")
def saved_words_handler(user_id: Annotated[int | None, Query()] = None):
    if user_id == None or user_id < 0:
        return error_result(err_msg="no user id or id is incorrect")
    return get_saved_words(user_id=user_id)


@app.delete("/saved_word", description="delete saved word from learning set")
def saved_removal_handler(saved_id: Annotated[int | None, Query()] = None):
    if saved_id == None:
        return error_result(err_msg="no saved id provided")
    return delete_saved_word(saved_id=saved_id)


@app.get("/can-train")
def can_train_handler(user_id: Annotated[int | None, Query()] = None):
    if user_id == None:
        return error_result(err_msg="no user id")
    return check_can_train(user_id=user_id)


@app.post("/accuracy-score")
def accuracy_score_handler(image: Annotated[str | None, Form()] = None, target: Annotated[str | None, Form(description="accuracy for based on target/goal")] = None):
    if image == None:
        return error_result(err_msg="no base64 image")
    if target == None:
        return error_result(err_msg="no target")

    return score_accuracy(image=image, target=target)