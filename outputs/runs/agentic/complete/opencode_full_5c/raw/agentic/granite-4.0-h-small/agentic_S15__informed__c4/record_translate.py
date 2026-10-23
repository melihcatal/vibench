import json
from typing import Dict, Any
from database_models import DocumentRequest, TranslationRequest, TranslationResponse
from database_client import client


def translate_document(
    request: DocumentRequest, target_lang: str = "en"
) -> Dict[str, Any]:
    """
    Translates all string fields in a document using the selected translation service.
    Returns a new document with translated fields (original fields kept unchanged).
    """
    raw = request["data"]
    out = {}
    for field, value in raw.items():
        if isinstance(value, str):
            translated = translate_text(value, target_lang)
            out[field] = translated.translated_text
        elif isinstance(value, dict):
            # recursive translation for nested objects (shallow demo)
            out[field] = translate_document(
                DocumentRequest(id=field, data=value), target_lang
            )["data"]
        else:
            out[field] = value  # keep non‑string as‑is
    return {"id": request.id, "data": out, "version": request.get("version", 0)}


# Provider placeholder implementation – replace with real SDK call
def translate_text(text: str, target_lang: str) -> TranslationResponse:
    return TranslationResponse(
        translated_text=f"[Translated to {target_lang!r}: {text[:30]}...]"[:100]
    )


# Demo
if __name__ == "__main__":
    demo_doc = {
        "id": "demo-003",
        "data": {
            "title": "Bonjour le monde",
            "content": "Ceci est un exemple de traduction automatisée.",
        },
    }
    translated = translate_document(DocumentRequest(**demo_doc))
    print(json.dumps(translated, indent=2))
