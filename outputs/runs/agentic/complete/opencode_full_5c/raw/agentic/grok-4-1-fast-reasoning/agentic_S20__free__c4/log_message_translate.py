import os
import requests


def translate_log_message(message: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    params = {"auth_key": auth_key, "text": message, "target_lang": target_lang}
    response = requests.post(url, data=params)
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
