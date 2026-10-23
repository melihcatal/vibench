import os
import requests
from typing import Dict, Any, List, Optional

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str = "EN") -> str:
    params = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "target_lang": target_lang.upper(),
    }
    response = requests.post(DEEPL_API_URL, data=params)
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]


def translate_document_fields(
    document: Dict[str, Any], fields: List[str], target_lang: str = "EN"
) -> Dict[str, Any]:
    translated_doc = document.copy()
    for field in fields:
        if field in document and isinstance(document[field], str):
            try:
                translated_doc[field] = translate_text(document[field], target_lang)
            except:
                pass
    return translated_doc
