import os
import requests

def translate_appeal(appeal_text: str, target_lang: str = "EN") -> str:
    """
    Translates appeal text for review using DeepL API.
    """
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "text": appeal_text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    data = response.json()
    return data["translations"][0]["text"]
