from __future__ import annotations

from typing import List

from document_client import get_client, normalize_source
from document_models import KeyValuePair


def extract_key_values(source: str) -> List[KeyValuePair]:
    client = get_client()
    payload = normalize_source(source)
    poller = client.begin_analyze_document(model_id="prebuilt-document", body=payload)
    result = poller.result()
    pairs: List[KeyValuePair] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "")
        value = getattr(getattr(kv, "value", None), "content", "")
        pairs.append(KeyValuePair(key=key, value=value, confidence=getattr(kv, "confidence", None)))
    return pairs
