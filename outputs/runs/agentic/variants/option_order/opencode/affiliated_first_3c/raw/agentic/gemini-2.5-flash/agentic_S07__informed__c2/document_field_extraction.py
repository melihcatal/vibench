from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentRequest
from typing import Dict, Any


def extract_structured_fields(request: DocumentRequest) -> Dict[str, Any]:
    client = get_documentai_client()
    # For invoice parsing, you typically use a pre-trained processor, e.g., "invoice-parser"
    # The processor_id in DocumentRequest should correspond to an invoice parser processor.
    processor_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )

    raw_document = documentai.RawDocument(
        content=request.file_content,
        mime_type=request.mime_type,
    )
    request_options = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request_options)

    extracted_fields = {}
    for entity in result.document.entities:
        # Accessing normalized values and confidence scores
        value = (
            client.get_text(result.document.text, entity.text_anchor)
            if entity.text_anchor
            else ""
        )

        # Example of extracting common invoice fields
        if entity.type_ == "invoice_id":
            extracted_fields["invoice_id"] = value
        elif entity.type_ == "total_amount":
            extracted_fields["total_amount"] = {
                "value": value,
                "currency": entity.currency.currency_code if entity.currency else "",
            }
        elif entity.type_ == "supplier_name":
            extracted_fields["supplier_name"] = value
        # Add more field extractions as needed based on the processor's entity types

    return extracted_fields
