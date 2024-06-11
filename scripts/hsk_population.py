from selenium.webdriver import Chrome, ChromeService
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from deep_translator import GoogleTranslator

from typing import Dict
import sys
import os

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)

from database.chinesebee_db import db_conn
from utils.decorators import tireless_connection


def scrape_words(level: int) -> list[Dict]:
    chrome = Chrome(service=ChromeService(ChromeDriverManager().install()))

    chrome.get(f"https://mandarinbean.com/new-hsk-{level}-word-list/")

    table = chrome.find_element(
        by=By.CLASS_NAME, value="has-subtle-pale-blue-background-color"
    )
    table_body = table.find_element(by=By.TAG_NAME, value="tbody")
    table_content = table_body.find_elements(by=By.TAG_NAME, value="tr")

    print(f"found table content {len(table_content)}")

    words = []
    translator = GoogleTranslator(source="en", target="ru")
    for row in table_content:
        row_content = row.find_elements(by=By.TAG_NAME, value="td")
        words.append(
            {
                "chinese": row_content[1].text,
                "pinyin": row_content[2].text,
                "english": row_content[3].text,
                "russian": translator.translate(row_content[3].text),
                "level": level,
            }
        )
    print(words[0])
    return words



@tireless_connection
def populate_database_with_words():
    hsk_collections: list[list[Dict]] = []
    for level in range(6):
        hsk_words = scrape_words(level=level+1)
        hsk_collections.append(hsk_words)
    
    with db_conn.cursor() as cursor:
        # todo: insert all hsk words into db
        # for all collections, insert all words
        for collection in hsk_collections:
            words_values = [f"('{word["chinese"]}', '{word["pinyin"]}', '{word["english"]}', '{word["russian"]}', {word["level"]})" for word in collection]
            cursor.execute(f"insert into hsk_words(chinese, pinyin, english, russian, hsk_level) values {", ".join(words_values)}")
        db_conn.commit()

populate_database_with_words()