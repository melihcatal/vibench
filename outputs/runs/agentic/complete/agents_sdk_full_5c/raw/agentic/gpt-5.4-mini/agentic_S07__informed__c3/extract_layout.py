from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, choose_model, request_to_stream
from document_models import DocumentLayoutElement, DocumentLayoutResult, DocumentRequest, normalize_text


def extract_layout(request: DocumentRequest) -> DocumentLayoutResult:
    client = build_client()
    source = request_to_stream(request)
    model_id = choose_model(request)
    if isinstance(source, str):
        poller = client.begin_analyze_document(model_id, AnalyzeDocumentRequest(url_source=source))
    else:
        poller = client.begin_analyze_document(model_id, body=source)
    result = poller.result()
    elements = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            elements.append(DocumentLayoutElement(kind="line", text=normalize_text(getattr(line, "content", "")), confidence=getattr(line, "confidence", None), raw=line))
        for table in getattr(result, "tables", []) or []:
            elements.append(DocumentLayoutElement(kind="table", text="", confidence=getattr(table, "confidence", None), row_count=len(getattr(table, "cells", []) or []), raw=table))
    if not elements and getattr(result, "content", None):
        elements.append(DocumentLayoutElement(kind="text", text=normalize_text(result.content), raw=result))
    return DocumentLayoutResult(elements=elements, provider="azure-ai-documentintelligence", raw=result)
