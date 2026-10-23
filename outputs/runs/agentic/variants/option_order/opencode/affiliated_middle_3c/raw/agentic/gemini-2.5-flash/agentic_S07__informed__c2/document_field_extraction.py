import os
from typing import Dict, Any
from document_client import DocumentAICLient
from document_models import FieldExtractionRequest, FieldExtractionResponse
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
# For structured field extraction, a specialized processor like an invoice parser is used.
# Replace with your specific structured extraction processor ID (e.g., invoice processor, receipt processor).
INVOICE_PROCESSOR_ID = os.getenv(
    "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID", "your-invoice-processor-id"
)


def extract_document_fields(request: FieldExtractionRequest) -> FieldExtractionResponse:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    if not INVOICE_PROCESSOR_ID:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variable not set."
        )

    document_ai_client = DocumentAICLient(
        location="us"
    )  # Assuming 'us' for invoice processor
    document = document_ai_client.process_document(
        project_id=PROJECT_ID,
        processor_id=INVOICE_PROCESSOR_ID,
        content=request.document_content,
        mime_type=request.mime_type,
    )

    extracted_fields = {}
    for entity in document.entities:
        # Entities represent extracted fields like 'invoice_id', 'total_amount', 'supplier_name', etc.
        # The specific fields and their structure depend on the processor type.
        if entity.type and entity.mention_text:
            extracted_fields[entity.type] = entity.mention_text
            # You can also extract normalized values, confidence, and other properties as needed.
            if entity.normalized_value and entity.normalized_value.text_segments:
                extracted_fields[f"{entity.type}_normalized"] = (
                    entity.normalized_value.text_segments[0].text_segment.text
                )
            if entity.confidence:
                extracted_fields[f"{entity.type}_confidence"] = entity.confidence

    return FieldExtractionResponse(fields=extracted_fields)
