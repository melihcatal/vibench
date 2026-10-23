from typing import Dict
from database_models import Document
import os

# Placeholder for real translation using Google Gemini (LLM) as a translator
# In a real implementation replace with Gemini API call.

TRANSLATOR_ENDPOINT = os.getenv("GOOGLE_AI_TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("GOOGLE_API_KEY")

VALID_TARGETS = {"es", "fr", "de", "zh", "ja"}


def translate_document(doc: Document, target_lang: str) -> Document:
    """
    Translate user-facing text fields in the document to the target language.
    Returns a new Document with translations applied.
    """
    if target_lang not in VALID_TARGETS:
        raise ValueError(f"Unsupported target language: {target_lang}")
    # Simulated translation: prepend "[lang] " to demonstrate the idea.
    translated = {}
    for k, v in doc["data"].items():
        if isinstance(v, str):
            translated[k] = f"[{target_lang}] {v}"
        else:
            translated[k] = v
    return {
        "id": doc["id"],
        "data": translated,
    }
