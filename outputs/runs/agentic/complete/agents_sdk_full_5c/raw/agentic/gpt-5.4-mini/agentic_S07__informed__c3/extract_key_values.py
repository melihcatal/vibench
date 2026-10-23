from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, choose_model, request_to_stream
from document_models import DocumentKeyValuePair, DocumentKeyValueResult, DocumentRequest, normalize_key, normalize_text


def extract_key_values(request: DocumentRequest) -> DocumentKeyValueResult:
    client = build_client()
    source = request_to_stream(request)
    model_id = choose_model(request)
    if isinstance(source, str):
        poller = client.begin_analyze_document(model_id, AnalyzeDocumentRequest(url_source=source))
    else:
        poller = client.begin_analyze_document(model_id, body=source)
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = normalize_key(getattr(getattr(kv, "key", None), "content", ""))
        value = normalize_text(getattr(getattr(kv, "value", None), "content", ""))
        if key or value:
            pairs.append(DocumentKeyValuePair(key=key, value=value, confidence=getattr(kv, "confidence", None), raw=kv))
    return DocumentKeyValueResult(pairs=pairs, provider="azure-ai-documentintelligence", raw=result)
