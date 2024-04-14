from fastapi import FastAPI, Path
from typing import Annotated

from api.chinese_search import get_chinese_match

app = FastAPI()


@app.get("/")
async def root():
    return {
        "status": "alive"
    }

@app.get("/chinese-match/{word}")
def chinese_match(word: Annotated[str, Path(description="word for which to find chinese word")]):
    if word == "":
        return {
            "status": "error",
            "error": "no word provided"
        }
    return get_chinese_match(word=word + "\n")
    