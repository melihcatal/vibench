from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_intelligence_client
from document_models import DocumentRequest, normalize_layout_items


MODEL_ID = 'prebuilt-layout'


def extract_layout(document: DocumentRequest | str, content_type: str | None = None):
    source = document.source if isinstance(document, DocumentRequest) else document
    ctype = document.content_type if isinstance(document, DocumentRequest) else content_type
    client = create_document_intelligence_client()
    with open(source, 'rb') as stream:
        poller = client.begin_analyze_document(MODEL_ID, analyze_request=AnalyzeDocumentRequest(bytes_source=stream.read()), content_type=ctype or 'application/pdf')
    result = poller.result()
    return normalize_layout_items(getattr(result, 'paragraphs', None) or getattr(result, 'pages', None) or [])
