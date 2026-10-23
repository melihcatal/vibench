import requests
import os


def translate_log_message(log_message: str, target_lang: str = "es") -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY not set")
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    data = {"q": log_message, "target": target_lang}
    response = requests.post(url, data=data)
    response.raise_for_status()
    translated_text = response.json()["data"]["translations"][0]["translatedText"]
    return translated_text
