import os
from google.cloud import translate_v2 as translate

# Provider credentials
TRANSLATOR_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # path to service account JSON

TRANSLATOR = translate.Client() if TRANSLATOR_KEY else None


def translate_vendor_note(note: str, target_lang: str = "en") -> str:
    """Translate the invoice description/memo field to the target language."""
    if not TRANSLATOR:
        raise RuntimeError("Google Translate client not configured")
    result = TRANSLATOR.translate(text=note, target_language=target_lang)
    return result["translatedText"]
