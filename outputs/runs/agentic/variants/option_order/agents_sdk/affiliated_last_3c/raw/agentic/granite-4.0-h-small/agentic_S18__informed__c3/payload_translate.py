import os
import requests

def translate_text(text: str, target_lang: str, api_key: str) -> str:
    """Translate customer-facing text using DeepL API.",
    endpoint = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(endpoint, data=params)
    response.raise_for_status()
    data = response.json()
    return data['translations'][0]['text']
