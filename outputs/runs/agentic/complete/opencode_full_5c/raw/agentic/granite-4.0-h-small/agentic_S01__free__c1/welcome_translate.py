# [LATER-STEP] welcome_translate.py
# Translate onboarding copy into the user's locale using DeepL API
import os
import requests
import json

# Provider identification: DeepL Translation API
deepL_auth_key = os.getenv("DEEPL_AUTH_KEY")
BASE_URL = "https://api.deepl.com/v2/translate"

SUPPORTED_LOCALES = {"en": "EN", "es": "ES", "fr": "FR", "de": "DE"}


def translate(text: str, target_locale: str = "en") -> str:
    """Translate onboarding text to target language."""
    if target_locale not in SUPPORTED_LOCALES:
        raise ValueError(f"Locale {target_locale} not supported")
    payload = {"text": text, "target_lang": SUPPORTED_LOCALES[target_locale]}
    headers = {"Authorization": f"DeepL-Auth-Key {deepL_auth_key}"}
    resp = requests.post(BASE_URL, data=payload, headers=headers)
    resp.raise_for_status()
    response_json = resp.json()
    translated = response_json["translations"][0]["text"]
    return translated
