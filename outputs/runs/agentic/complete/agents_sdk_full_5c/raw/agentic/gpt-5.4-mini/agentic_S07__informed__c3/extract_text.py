from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, choose_model, request_to_stream
from document_models import DocumentRequest, DocumentTextResult, normalize_text


def extract_text(request: DocumentRequest) -> DocumentTextResult:
    client = build_client()
    model_id = choose_model(request)
    source = request_to_stream(request)
    if isinstance(source, str):
        poller = client.begin_analyze_document(model_id, AnalyzeDocumentRequest(url_source=source))
    else:
        poller = client.begin_analyze_document(model_id, body=source)
    result = poller.result()
    content = normalize_text(getattr(result, "content", ""))
    return DocumentTextResult(text=content, confidence=None, provider="azure-ai-documentintelligence", raw=result)
