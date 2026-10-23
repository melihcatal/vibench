import os
import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def moderation_summary(text):
    url = "https://api.deepl.com/v2/translate"
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"}
    data = {"text": text, "target_lang": "EN"}
    response = requests.post(url, headers=headers, data=data)
    return response.json()["translations"][0]["text"]
