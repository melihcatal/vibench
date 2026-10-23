from __future__ import annotations

from typing import List, Union

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_client
from document_models import DocumentInput, KeyValueExtractionResult, KeyValuePair

PROVIDER = "azure-document-intelligence"
MODEL_ID = "prebuilt-document"


def extract_key_values(document: Union[DocumentInput, str]) -> KeyValueExtractionResult:
    client = get_client()
    source_url = document.source_url if isinstance(document, DocumentInput) else str(document)
    poller = client.begin_analyze_document(model_id=MODEL_ID, analyze_request=AnalyzeDocumentRequest(url_source=source_url))
    result = poller.result()
    pairs: List[KeyValuePair] = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "") or ""
        value = getattr(getattr(kv, "value", None), "content", "") or ""
        pairs.append(KeyValuePair(key=key, value=value, confidence=getattr(kv, "confidence", None)))
    return KeyValueExtractionResult(pairs=pairs, provider=PROVIDER, model_id=MODEL_ID)
