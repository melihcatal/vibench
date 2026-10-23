# [LATER-STEP] invoice_note_translate.py
# Translate extracted invoice notes or descriptions

from google.cloud import translate_v2 as translate
from typing import Dict


def translate_invoice_note(note: str, target_lang: str = "en") -> Dict[str, str]:
    """
    Translate a raw note to the target language using Google Cloud Translation
    (requires GOOGLE_APPLICATION_CREDENTIALS configured).
    Returns a dict with original and translated text.
    """
    client = translate.Client()
    result = client.translate(note, target_language=target_lang)
    return {
        "original": note,
        "translated": result["translatedText"],
        "detected_source_language": result["sourceLanguage"],
    }
