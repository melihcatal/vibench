from __future__ import annotations

from typing import Any, Dict, List

from document_client import build_document_analysis_client
from document_models import KeyValueResponse, normalize_key_value_pairs

AZURE_FORM_MODEL = "prebuilt-document"


def extract_key_values(document_bytes: bytes) -> KeyValueResponse:
    client = build_document_analysis_client()
    poller = client.begin_analyze_document(AZURE_FORM_MODEL, document=document_bytes)
    result = poller.result()

    pairs: List[Dict[str, Any]] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pairs.append({
            "key": getattr(getattr(kv, "key", None), "content", ""),
            "value": getattr(getattr(kv, "value", None), "content", ""),
            "confidence": getattr(kv, "confidence", 0.0),
        })

    return KeyValueResponse(pairs=normalize_key_value_pairs(pairs), raw=getattr(result, "to_dict", lambda: None)())
