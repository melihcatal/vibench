from google.cloud import documentai
from document_client import get_documentai_client, build_process_document_request
from document_models import normalize_document_fields

def invoice_summary(payload, config=None):
    config = config or {}
    request = build_process_document_request(config, payload)
    client = get_documentai_client(config)
    response = client.process_document(request=request)
    fields = {entity.type_: entity.mention_text for entity in response.document.entities}
    normalized_fields = normalize_document_fields(fields)
    summary = {
        "vendor": normalized_fields.get("vendor"),
        "date": normalized_fields.get("date"),
        "total": normalized_fields.get("total"),
        "items": normalized_fields.get("items")
    }
    return summary