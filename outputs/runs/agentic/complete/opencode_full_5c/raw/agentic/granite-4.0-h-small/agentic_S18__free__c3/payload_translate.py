import json

# [LATER-STEP] payload_translate.py
# Translate customer-facing message payload text using a mock translation service

TRANSLATIONS = {
    "en": {"welcome": "Welcome", "thank_you": "Thank you"},
    "es": {"welcome": "Bienvenido", "thank_you": "Gracias"},
}


def translate_payload(payload: dict, target_lang: str = "es") -> dict:
    """Translate simple key/value text fields inside a payload."""
    lang_dict = TRANSLATIONS.get(target_lang, TRANSLATIONS["en"])
    translated = payload.copy()
    for key, default in [("welcome", "Welcome"), ("thank_you", "Thank you")]:
        if payload.get(key):
            translated[key] = lang_dict.get(key, default)
    return translated
