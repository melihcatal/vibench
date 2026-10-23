# [LATER-STEP] invoice_note_translate.py
# Translate extracted invoice notes or descriptions using DeepL API

import os
import json
import requests
from document_models import NormalizedExpense


def translate_note(note_text: str, target_lang: str = "en") -> str:
    """Translate a text string using DeepL API.

    Returns translated text.\n"""
    url = "https://api.deepl.com/v2/translate"
    payload = {
        "auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "text": note_text,
        "target_lang": target_lang,
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["translations"][0]["text"]
