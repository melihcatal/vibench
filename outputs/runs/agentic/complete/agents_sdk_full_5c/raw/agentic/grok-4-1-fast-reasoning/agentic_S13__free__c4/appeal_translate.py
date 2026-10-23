import requests
from safety_client import GOOGLE_TRANSLATE_KEY

def appeal_translate(text: str, target_language: str = "en") -> str:
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": GOOGLE_TRANSLATE_KEY,
        "q": text,
        "target": target_language
    }
    response = requests.get(url, params=params).json()
    return response["data"]["translations"][0]["translatedText"]