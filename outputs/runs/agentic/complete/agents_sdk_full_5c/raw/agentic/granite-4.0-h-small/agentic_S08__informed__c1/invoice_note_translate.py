import os
import requests
from typing import TypedDict
import json
from document_models import InvoiceDocument

# Minimal translation client using DeepL REST API

class TranslationResult(TypedDict):
    translated_text: str


def invoice_note_translate(text: str) -> str:
    deepl_key = os.getenv('DEEPL_AUTH_KEY')
    url = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': deepl_key,
        'text': text,
        'target_lang': 'EN'
    }
    resp = requests.post(url, data=params)
    resp.raise_for_status()
    data = resp.json()
    return data['translations'][0]['text']
