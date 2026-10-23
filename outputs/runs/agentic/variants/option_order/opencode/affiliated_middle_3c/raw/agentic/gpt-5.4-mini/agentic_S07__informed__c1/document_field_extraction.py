from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_intelligence_client


MODEL_ID = 'prebuilt-read'


def extract_document_fields(source: str, content_type: str | None = None):
    client = create_document_intelligence_client()
    with open(source, 'rb') as stream:
        poller = client.begin_analyze_document(MODEL_ID, analyze_request=AnalyzeDocumentRequest(bytes_source=stream.read()), content_type=content_type or 'application/pdf')
    result = poller.result()
    return {'text': getattr(result, 'content', ''), 'fields': [{'name': 'document_type', 'value': getattr(result, 'documents', [{}])[0].get('doc_type') if getattr(result, 'documents', None) else None}]}
