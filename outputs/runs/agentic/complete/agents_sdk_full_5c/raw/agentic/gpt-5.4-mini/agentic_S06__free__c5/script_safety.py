from __future__ import annotations

from google.cloud import language_v1

from speech_models import normalize_text


def check_script_safety(text: str) -> dict:
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_text(text), type_=language_v1.Document.Type.PLAIN_TEXT)
    moderation = client.moderate_text(request={"document": document})
    categories = []
    for cat in getattr(moderation, "moderation_categories", []):
        categories.append({"name": cat.name, "confidence": cat.confidence})
    return {"blocked": any(getattr(cat, "confidence", 0.0) > 0.8 for cat in getattr(moderation, "moderation_categories", [])), "categories": categories}
