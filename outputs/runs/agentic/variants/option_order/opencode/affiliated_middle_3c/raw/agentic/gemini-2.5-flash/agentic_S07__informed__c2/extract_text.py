import os
from typing import Dict, Any
from document_client import DocumentAICLient
from document_models import DocumentExtractionRequest, TextExtractionResponse

# Google Document AI processor ID for general document processing
# Replace with your specific processor ID or use a general one like 'OCR_PROCESSOR_ID'
# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
GENERAL_PROCESSOR_ID = os.getenv(
    "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID", "your-general-processor-id"
)


def extract_text_from_document(
    request: DocumentExtractionRequest,
) -> TextExtractionResponse:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    if not GENERAL_PROCESSOR_ID:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID environment variable not set."
        )

    document_ai_client = DocumentAICLient(location=request.location)
    document = document_ai_client.process_document(
        project_id=PROJECT_ID,
        processor_id=request.processor_id
        if request.processor_id != ""
        else GENERAL_PROCESSOR_ID,
        content=request.content,
        mime_type=request.mime_type,
    )
    return TextExtractionResponse(text=document.text)
