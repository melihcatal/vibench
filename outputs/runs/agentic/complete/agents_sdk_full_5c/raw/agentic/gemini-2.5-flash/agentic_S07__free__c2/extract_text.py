from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, TextExtractionResponse

def extract_text(request: DocumentProcessingRequest) -> TextExtractionResponse:
    """Extracts plain text from a scanned document image using Google Cloud Document AI."""
    client = get_documentai_client()
    
    # The processor ID can be a generic one for text extraction, e.g., "OCR_PROCESSOR_V1"
    # or a more general one like "FORM_PARSER_PROCESSOR_V1" if it's generally available.
    # For plain text, OCR_PROCESSOR_V1 is most appropriate.
    processor_id = "OCR_PROCESSOR_V1"  
    name = client.processor_path(request.project_id, request.location, processor_id)

    # Convert the base64 content to bytes
    document = documentai.RawDocument(content=request.file_content, mime_type=request.mime_type)

    process_options = documentai.ProcessOptions(
        ocr_config=documentai.OcrConfig(enable_native_pdf_parsing=True)
    )

    response = client.process_document(
        name=name,
        raw_document=document,
        process_options=process_options
    )

    full_text = response.document.text
    return TextExtractionResponse(text=full_text)
