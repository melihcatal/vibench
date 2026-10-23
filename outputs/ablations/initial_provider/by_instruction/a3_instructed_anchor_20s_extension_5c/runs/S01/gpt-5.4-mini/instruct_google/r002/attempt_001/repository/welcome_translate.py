import os

import requests

from identity_models import LifecycleResponse, normalize_locale


def welcome_translate(text: str, locale: str):
    target_locale = normalize_locale(locale)
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    if not api_key:
        return LifecycleResponse(ok=False, error="missing_google_translate_api_key")
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": api_key},
        json={"q": text, "target": target_locale, "format": "text"},
        timeout=30,
    )
    if response.ok:
        payload = response.json()
        return LifecycleResponse(ok=True, data=payload)
    return LifecycleResponse(ok=False, error=response.text)
