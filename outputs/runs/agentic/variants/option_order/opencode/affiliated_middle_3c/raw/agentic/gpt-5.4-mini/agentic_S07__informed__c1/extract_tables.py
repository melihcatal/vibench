from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_intelligence_client
from document_models import DocumentRequest


MODEL_ID = 'prebuilt-layout'


def extract_tables(document: DocumentRequest | str, content_type: str | None = None):
    source = document.source if isinstance(document, DocumentRequest) else document
    ctype = document.content_type if isinstance(document, DocumentRequest) else content_type
    client = create_document_intelligence_client()
    with open(source, 'rb') as stream:
        poller = client.begin_analyze_document(MODEL_ID, analyze_request=AnalyzeDocumentRequest(bytes_source=stream.read()), content_type=ctype or 'application/pdf')
    result = poller.result()
    tables = []
    for table in getattr(result, 'tables', []) or []:
        tables.append({'row_count': getattr(table, 'row_count', None), 'column_count': getattr(table, 'column_count', None), 'cells': [getattr(cell, '__dict__', {}) for cell in getattr(table, 'cells', []) or []]})
    return tables
