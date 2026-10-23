# translation_models.py
from typing import TypedDict

class TranslationRequest(TypedDict):
    source_text: str
    source_lang: str
    target_lang: str

class TranslationResponse(TypedDict):
    translated_text: str

def normalize_response(resp_text: str) -> str:
    """Post‑process translation output (e.g., trim whitespace, normalize quotes)."""
    return resp_text.strip().replace('\u2018', '\"').replace('\u2019', '\"')
