import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TRANSLATE_API_KEY_ENV = "GOOGLE_TRANSLATE_API_KEY"
GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


class WelcomeTranslateError(RuntimeError):
    pass


def translate_welcome_copy(text: str, target_locale: str, source_locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get(GOOGLE_TRANSLATE_API_KEY_ENV)
    if not api_key:
        raise WelcomeTranslateError("Missing Google Translate API key")

    params: Dict[str, Any] = {"q": text, "target": target_locale, "key": api_key, "format": "text"}
    if source_locale:
        params["source"] = source_locale

    response = requests.get(GOOGLE_TRANSLATE_ENDPOINT, params=params, timeout=30)
    if response.status_code >= 400:
        raise WelcomeTranslateError(f"Google Translate request failed: {response.status_code} {response.text}")

    data = response.json()
    translations = data.get("data", {}).get("translations", [])
    if not translations:
        raise WelcomeTranslateError("Google Translate response missing translations")

    translated_text = translations[0].get("translatedText")
    if not translated_text:
        raise WelcomeTranslateError("Google Translate response missing translatedText")

    return {"text": translated_text, "target_locale": target_locale, "provider": "google_translate", "raw": data}
