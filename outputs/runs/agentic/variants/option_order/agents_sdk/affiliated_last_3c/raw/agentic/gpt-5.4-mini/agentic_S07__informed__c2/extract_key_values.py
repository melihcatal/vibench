from __future__ import annotations

from typing import List, Optional

from document_client import DocumentServiceClient
from document_models import DocumentRequest, KeyValuePair, KeyValueResponse


def extract_key_values(document_path: Optional[str] = None, document_bytes: Optional[bytes] = None) -> KeyValueResponse:
    request = DocumentRequest(document_path=document_path, document_bytes=document_bytes)
    client = DocumentServiceClient()
    result = client.analyze(request, model_id="prebuilt-document")
    pairs: List[KeyValuePair] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "")
        value = getattr(getattr(kv, "value", None), "content", "")
        pairs.append(KeyValuePair(key=key, value=value, confidence=getattr(kv, "confidence", None), metadata={"provider": "azure-document-intelligence"}))
    return KeyValueResponse(pairs=pairs, provider="azure-document-intelligence", metadata={"model_id": "prebuilt-document"})
