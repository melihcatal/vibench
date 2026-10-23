import os
import requests
from observability_client import get_cached_client

def translate_log_message(message: str, target_locale: str = "es") -> str:
    """Translate support‑visible log messages to another locale using DeepL API.
    Args:
        message: Original log text.
        target_locale: Language code (e.g., 'es' for Spanish, 'fr' for French).
    Returns:
        The translated text.
    """
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY not set in environment")
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": message,
        "target_lang": target_locale.upper()
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
