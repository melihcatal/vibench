import os
import requests


def runbook_translate(text: str, target_lang: str) -> str | None:
    """
    Translate secret-rotation runbook notes using the DeepL API.
    """
    api_key = os.environ.get("DEEPL_API_KEY")
    url = "https://api-free.deepl.com/v2/translate"

    payload = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        translated_text = response.json()["translations"][0]["text"]
        return translated_text
    except requests.exceptions.RequestException as e:
        print(f"Error translating text: {e}")
        return None
