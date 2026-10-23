import os
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_intelligence_client
from document_models import DocumentRequest, normalize_response_text


MODEL_ID = 'prebuilt-read'


def extract_text(document: DocumentRequest | str, content_type: str | None = None) -> str:
    source = document.source if isinstance(document, DocumentRequest) else document
    ctype = document.content_type if isinstance(document, DocumentRequest) else content_type
    client = create_document_intelligence_client()
    with open(source, 'rb') as stream:
        poller = client.begin_analyze_document(MODEL_ID, analyze_request=AnalyzeDocumentRequest(bytes_source=stream.read()), content_type=ctype or 'application/pdf')
    result = poller.result()
    return normalize_response_text(getattr(result, 'content', result))
