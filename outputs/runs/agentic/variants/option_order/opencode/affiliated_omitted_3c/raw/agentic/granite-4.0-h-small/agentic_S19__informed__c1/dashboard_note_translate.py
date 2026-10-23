from observability_client import get_datadog_headers
import requests
from observability_models import TranslationResult

import os


def translate_dashboard_note(note: str, target_locale: str = "es") -> TranslationResult:
    """
    Translate a metric or dashboard note into another locale using DeepL.
    Returns the translated text in `TranslationResult.translated`.
    """
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "text": note,
        "target_lang": target_locale,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    res_json = resp.json()
    translated = res_json["translations"][0]["text"]
    return {
        "translated": translated,
    }
