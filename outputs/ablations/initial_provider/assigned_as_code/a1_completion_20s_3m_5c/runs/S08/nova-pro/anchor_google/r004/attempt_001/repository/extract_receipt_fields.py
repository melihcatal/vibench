from google.cloud import documentai
from document_client import get_documentai_client, build_process_document_request
from document_models import normalize_document_fields

def extract_receipt_fields(payload, config=None):
    config = config or {}
    request = build_process_document_request(config, payload)
    client = get_documentai_client(config)
    response = client.process_document(request=request)
    fields = {entity.type_: entity.mention_text for entity in response.document.entities}
    normalized_fields = normalize_document_fields(fields)
    return normalized_fields