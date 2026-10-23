import os
import requests
from model_client import get_openai_api_key

def translate_text(text: str, target_lang: str = "es", api_key: str = os.getenv("DEEPL_AUTH_KEY")) -> str:
    """Translate text using DeepL API.

    Returns translated string.
    """
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
    url = "https://api-free.deepl.com/v2/translate"
    payload = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    return resp.json()["translations"][0]["text"]

if __name__ == "__main__":
    sample = "Hello, world!"
    print(f"Translated: {translate_text(sample)}")
