import os
import requests
from document_models import Expense

def translate_notes(expense: Expense, target_lang: str = "en", translation_endpoint: str = "https://translation.googleapis.com/language/translate/v2", api_key: str = os.getenv("GOOGLE_TRANSLATE_API_KEY")) -> str:
    """Translates vendor or memo notes using Google Cloud Translation API."""
    vendor_note = expense.metadata.get("vendor_note", "")
    if not vendor_note:
        return vendor_note
    params = {
        "q": vendor_note,
        "target": target_lang,
        "format": "text",
        "key": api_key
    }
    response = requests.get(translation_endpoint, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Translation API error: {response.status_code}")
    data = response.json()
    translated = data["data"]["translations"][0]["translatedText"]
    return translated
