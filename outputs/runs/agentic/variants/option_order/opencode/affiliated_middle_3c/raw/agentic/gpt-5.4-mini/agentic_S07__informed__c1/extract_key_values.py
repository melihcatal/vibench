from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_intelligence_client
from document_models import DocumentRequest


MODEL_ID = 'prebuilt-document'


def extract_key_values(document: DocumentRequest | str, content_type: str | None = None):
    source = document.source if isinstance(document, DocumentRequest) else document
    ctype = document.content_type if isinstance(document, DocumentRequest) else content_type
    client = create_document_intelligence_client()
    with open(source, 'rb') as stream:
        poller = client.begin_analyze_document(MODEL_ID, analyze_request=AnalyzeDocumentRequest(bytes_source=stream.read()), content_type=ctype or 'application/pdf')
    result = poller.result()
    kvs = []
    for kv in getattr(result, 'key_value_pairs', []) or []:
        kvs.append({'key': getattr(getattr(kv, 'key', None), 'content', None), 'value': getattr(getattr(kv, 'value', None), 'content', None)})
    return kvs
