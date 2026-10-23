import os
from typing import Dict, Any

from database_client import get_firestore_client
from database_models import DocumentRequest, normalize_response

# Import the chosen translation provider – Gemini API as an example.
from google.generativeai import generative_model


def translate_field(payload: Dict[str, Any], target_lang: str = "es") -> Dict[str, Any]:
    """Translate selected text fields in a document payload.

    Uses the Gemini API for translation.
    """
    translated = {}
    for key, value in payload.items():
        if isinstance(value, str):
            # Geminiify translation call (simplified). In production wrap API key securely.
            translation = generative_model.generate_content(
                prompt=f"Translate the following text to {target_lang}: {value}",
                model="gemini-1.5-flash",
            ).text
            translated[key] = translation
        else:
            translated[key] = value
    return translated


def translate_document(req: DocumentRequest, target_lang: str = "es") -> Dict[str, Any]:
    """Translate fields of a stored document.

    Args:
        req: DocumentRequest providing identifier and possibly current payload.
        target_lang: Destination language code.
    Returns:
        Normalized document data with translated fields.
    """
    client = get_firestore_client()
    doc_ref = client.collection("documents").document(req.identifier)
    snapshot = doc_ref.get()
    if not snapshot.exists:
        raise ValueError(f"Document '{req.identifier}' not found")

    data = snapshot.to_dict()
    # Translate only string‑typed fields.
    translated_data = translate_field(data)
    return normalize_response({"id": req.identifier, **translated_data})
