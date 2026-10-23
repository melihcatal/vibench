# Translate extracted invoice notes or memo fields into a target language

from typing import Dict
from google.cloud import translate_v2 as translate

# Configure client via env variables (GOOGLE_APPLICATION_CREDENTIALS etc.)
translator = translate.Client()
TARGET_LANG = "es"  # Example target: Spanish


def translate_notes(expense: Dict) -> Dict:
    """
    Translate the `summary` or `notes` field of an expense record into TARGET_LANG.
    Returns the expense dict with an added `translated_notes` field.
    """
    notes = expense.get("summary", "")
    if not notes:
        return expense  # nothing to translate

    translation = translator.translate(notes, target_language=TARGET_LANG)
    translated = translation.get("translatedText", notes)
    expense["translated_notes"] = translated
    return expense
