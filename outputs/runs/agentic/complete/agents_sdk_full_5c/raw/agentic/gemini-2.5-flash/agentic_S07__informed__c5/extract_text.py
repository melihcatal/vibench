import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, DocumentTextExtractionResponse

def extract_plain_text(request: DocumentProcessingRequest) -> DocumentTextExtractionResponse:
    """Extracts plain text from a scanned document image using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(
        os.environ.get("GOOGLE_CLOUD_PROJECT"),
        os.environ.get("GOOGLE_CLOUD_LOCATION"),
        os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID_GENERAL") # Use a general processor
    )

    # Read the image file
    with open(request.document_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=request.mime_type
    )

    # Configure the process request
    request_docai = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    # Execute the OCR request
    result = client.process_document(request_docai)
    document = result.document

    return DocumentTextExtractionResponse(
        text_content=document.text
    )
