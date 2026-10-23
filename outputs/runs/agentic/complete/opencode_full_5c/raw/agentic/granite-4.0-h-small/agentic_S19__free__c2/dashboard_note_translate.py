# [LATER-STEP] dashboard_note_translate.py

import json
from google.cloud import translate_v2 as translate

# Provider client (Google Cloud Translation) – concrete provider identified
# In production you would instantiate this client once per module or via a utility.
translator = translate.Client()

# Mapping of locale codes to provider language codes (example)
LOCALE_MAP = {
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
    # add more as needed
}

def translate_dashboard_note(note_text: str, target_locale: str) -> str:
    \"\"\"Translate a dashboard or metric note into another locale.\n    Returns the translated text.\n    \"\"\"
    target_lang = LOCALE_MAP.get(target_locale, "en")
    if target_lang == "en":
        # No translation needed
        return note_text
    translation = translator.translate(note_text, target_language=target_lang)
    return translation["translatedText"]

# Example usage (not executed):
# translated = translate_dashboard_note("Sample note", "es")
# print(translated)
