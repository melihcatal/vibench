from document_client import get_document_intelligence_client
from document_models import FieldExtractionResult, DocumentProcessingRequest
import io

def extract_structured_fields(request: DocumentProcessingRequest) -> FieldExtractionResult:
    """
    Extracts structured fields from OCR-normalized document text using Azure Document Intelligence's prebuilt invoice model.
    """
    client = get_document_intelligence_client()

    if request.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-invoice", document_url=request.document_url
        )
    elif request.document_content and request.content_type:
        document_stream = io.BytesIO(request.document_content)
        poller = client.begin_analyze_document(
            "prebuilt-invoice", document_stream, content_type=request.content_type
        )
    else:
        raise ValueError("Either document_url or document_content and content_type must be provided.")

    result = poller.result()

    extracted_fields = {}
    if result.documents:
        # Assuming there's at least one document processed
        for doc in result.documents:
            for name, field in doc.fields.items():
                if field.value:
                    extracted_fields[name] = field.value
                elif field.content:
                    extracted_fields[name] = field.content
    
    return FieldExtractionResult(fields=extracted_fields)
