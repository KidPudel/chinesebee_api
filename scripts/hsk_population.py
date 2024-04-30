from selenium.webdriver import Chrome, ChromeService
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from deep_translator import GoogleTranslator

chrome = Chrome(service=ChromeService(ChromeDriverManager().install()))


level = 1

chrome.get(f"https://mandarinbean.com/new-hsk-{level}-word-list/")

table = chrome.find_element(
    by=By.CLASS_NAME, value="has-subtle-pale-blue-background-color"
)
table_body = table.find_element(by=By.TAG_NAME, value="tbody")
table_content = table_body.find_elements(by=By.TAG_NAME, value="tr")

words = []
translator = GoogleTranslator(source="en", target="ru")
for row in table_content:
    row_content = row.find_elements(by=By.TAG_NAME, value="td")
    words.append(
        {
            "chinese": row_content[1].text,
            "pinyin": row_content[2].text,
            "russian": translator.translate(row_content[3].text),
            "level": level,
        }
    )


print(words[0])
