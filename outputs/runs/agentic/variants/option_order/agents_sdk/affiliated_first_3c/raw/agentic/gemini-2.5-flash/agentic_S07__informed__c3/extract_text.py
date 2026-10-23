from document_client import get_documentai_client, get_processor_path
from document_models import DocumentRequest, TextExtractionResponse
from google.cloud.documentai_v1.types import RawDocument

def extract_text_from_document(
    document_request: DocumentRequest,
    project_id: str,
    location: str,
    processor_id: str,
) -> TextExtractionResponse:
    """
    Extracts plain text from a scanned document image using Google Document AI.
    """
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    raw_document = RawDocument(content=document_request.content, mime_type=document_request.mime_type)
    
    request = {"name": processor_path, "raw_document": raw_document}
    result = client.process_document(request=request)
    
    document = result.document
    return TextExtractionResponse(text_content=document.text)

