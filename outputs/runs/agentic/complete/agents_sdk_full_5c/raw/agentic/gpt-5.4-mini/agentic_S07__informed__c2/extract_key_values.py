from __future__ import annotations

from document_client import analyze_document, get_client
from document_models import DocumentInput, KeyValuePair, normalize_key_values

PROVIDER = "Azure AI Document Intelligence"
MODEL_ID = "prebuilt-document"


def extract_key_values(document_bytes: bytes, mime_type: str = "image/png") -> list[KeyValuePair]:
    client = get_client()
    document = DocumentInput(content=document_bytes, mime_type=mime_type)
    result = analyze_document(client, document, model_id=MODEL_ID)
    raw_pairs = []
    for kv in getattr(result, "key_value_pairs", []):
        raw_pairs.append(
            {
                "key": getattr(getattr(kv, "key", None), "content", ""),
                "value": getattr(getattr(kv, "value", None), "content", ""),
                "confidence": getattr(kv, "confidence", None),
            }
        )
    return normalize_key_values(raw_pairs)
