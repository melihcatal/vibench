from typing import Optional
import requests
import os
from pydantic import BaseModel

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


class TranslationResult(BaseModel):
    detected_source_language: str
    text: str


def translate_text(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> TranslationResult:
    """Translate text using DeepL API for multilingual embedding search."""
    if not DEEPL_API_KEY:
        raise ValueError("DEEPL_API_KEY environment variable is not set.")

    params = {"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang}

    if source_lang:
        params["source_lang"] = source_lang

    response = requests.post(DEEPL_API_URL, data=params)
    response.raise_for_status()

    result = response.json()["translations"][0]
    return TranslationResult(
        detected_source_language=result["detected_source_language"], text=result["text"]
    )


def multilingual_query_translate(
    query: str, target_lang: str, source_lang: Optional[str] = None
) -> str:
    """Translate a query for multilingual embedding search using DeepL API."""
    translation = translate_text(query, target_lang, source_lang)
    return translation.text
