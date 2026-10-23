import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path
from document_models import DocumentRequest, FieldExtractionResponse
from google.cloud.documentai_v1.types import RawDocument

def extract_structured_fields(
    document_request: DocumentRequest,
    project_id: str,
    location: str,
    processor_id: str, # e.g., for "invoice-parser"
) -> FieldExtractionResponse:
    """
    Extracts structured fields from OCR-normalized document text using a specialized
    Google Document AI processor (e.g., Invoice Parser).
    """
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    raw_document = RawDocument(content=document_request.content, mime_type=document_request.mime_type)
    
    request = {"name": processor_path, "raw_document": raw_document}
    result = client.process_document(request=request)
    
    document = result.document

    extracted_fields = {}
    for entity in document.entities:
        # For pre-trained processors like Invoice Parser, entities have specific types and properties
        field_value = None
        if entity.type == "invoice_id":
            field_value = entity.text_anchor.text_segments[0].content if entity.text_anchor.text_segments else None
        elif entity.type == "total_amount":
            field_value = float(entity.mention_text) if entity.mention_text else None # Assuming numeric
        elif entity.type == "supplier_name":
             field_value = entity.mention_text
        # Add more field types as needed based on the processor
        
        if field_value is not None:
            extracted_fields[entity.type] = field_value
            
    return FieldExtractionResponse(fields=extracted_fields)

