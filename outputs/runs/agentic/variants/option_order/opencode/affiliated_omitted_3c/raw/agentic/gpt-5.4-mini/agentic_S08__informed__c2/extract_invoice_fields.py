from google.cloud import documentai_v1 as documentai

from document_client import document_ai_processor_name, load_document_config
from document_models import DocumentRequest


def extract_invoice_fields(request: DocumentRequest):
    config = load_document_config()
    client = documentai.DocumentProcessorServiceClient()
    raw_document = documentai.RawDocument(
        content=request.content or b"", mime_type=request.mime_type
    )
    response = client.process_document(
        request={
            "name": document_ai_processor_name(config),
            "raw_document": raw_document,
        }
    )
    entity_map = {entity.type_: entity for entity in response.document.entities}
    return {
        "vendor": getattr(entity_map.get("supplier_name"), "mention_text", None),
        "date": getattr(entity_map.get("invoice_date"), "mention_text", None),
        "total": getattr(entity_map.get("total_amount"), "mention_text", None),
        "line_items": [
            {
                "description": getattr(item, "description", None),
                "amount": getattr(item, "amount", None),
            }
            for item in getattr(response.document, "line_items", [])
        ],
    }
