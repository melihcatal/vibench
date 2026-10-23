import io
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_document_client, load_document_config
from document_models import extract_layout as normalize_layout, normalize_payload


def extract_layout(payload, config=None):
    payload = normalize_payload(payload)
    config = load_document_config(config)
    with create_document_client(config) as client:
        result = client.begin_analyze_document('prebuilt-layout', AnalyzeDocumentRequest(bytes_source=payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'layout': normalize_layout(result)}
