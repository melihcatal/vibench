import os
import requests
from typing import TypedDict

# Example: Translate onboarding copy into the user's locale using DeepL API
# Requires environment variable DEEPL_AUTH_KEY to be set


class TranslateRequest(TypedDict):
    text: str
    target_lang: str  # ISO 639-1 code, e.g., "fr"


class TranslateResponse(TypedDict):
    translatedText: str


DEEPL_URL = "https://api.deepl.com/v2/translate"


def translate(text: str, target_lang: str, auth_key: str) -> str:
    """Translate text via the DeepL Translate API.

    Parameters:
        text (str): The source text to translate.
        target_lang (str): Destination language code.
        auth_key (str): DeepL authentication key.

    Returns:
        str: Translated text.
    """
    payload = {"text": text, "target_lang": target_lang, "auth_key": auth_key}
    try:
        resp = requests.post(DEEPL_URL, data=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data["translations"][0]["text"]
    except requests.RequestException as e:
        raise RuntimeError(f"DeepL translation failed: {e}")


# Example usage (not executed during file creation):
# response = translate('Welcome!', 'fr', os.getenv('DEEPL_AUTH_KEY'))
