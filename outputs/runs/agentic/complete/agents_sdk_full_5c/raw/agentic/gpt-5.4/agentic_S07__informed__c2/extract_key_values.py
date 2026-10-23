from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_DOCUMENT_MODEL, get_document_client, load_document_bytes
from document_models import KeyValueModel, KeyValuesResult


def extract_key_values(document_path: str, model_id: str = DEFAULT_DOCUMENT_MODEL) -> KeyValuesResult:
    client = get_document_client()
    body = AnalyzeDocumentRequest(bytes_source=load_document_bytes(document_path))
    poller = client.begin_analyze_document(model_id=model_id, body=body)
    result = poller.result()

    pairs = []
    for pair in result.key_value_pairs or []:
        key_obj = getattr(pair, "key", None)
        value_obj = getattr(pair, "value", None)
        pairs.append(
            KeyValueModel(
                key=getattr(key_obj, "content", "") if key_obj else "",
                value=getattr(value_obj, "content", "") if value_obj else "",
                confidence=getattr(pair, "confidence", None),
            )
        )

    return KeyValuesResult(pairs=pairs, provider="azure-document-intelligence", model_id=model_id)
