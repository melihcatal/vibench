from __future__ import annotations

from document_client import ensure_bytes, get_document_intelligence_client
from document_models import KeyValuePair, KeyValueResult


def extract_key_values(document_bytes: bytes, model_id: str = "prebuilt-document") -> KeyValueResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(model_id=model_id, body=ensure_bytes(document_bytes))
    result = poller.result().as_dict()

    pairs = []
    for item in result.get("keyValuePairs", []):
        key = (item.get("key") or {}).get("content", "")
        value = (item.get("value") or {}).get("content", "")
        confidence = item.get("confidence")
        page = None
        regions = (item.get("key") or {}).get("boundingRegions") or []
        if regions:
            page = regions[0].get("pageNumber")
        pairs.append(KeyValuePair(key=key, value=value, confidence=confidence, page=page))

    return KeyValueResult(provider="azure-document-intelligence", pairs=pairs, raw=result)
