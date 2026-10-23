from document_client import get_document_intelligence_client
from document_models import ExtractedTextResult, DocumentProcessingRequest
import io

def extract_plain_text(request: DocumentProcessingRequest) -> ExtractedTextResult:
    """
    Extracts plain text from a scanned document image using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    if request.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-read", document_url=request.document_url
        )
    elif request.document_content and request.content_type:
        document_stream = io.BytesIO(request.document_content)
        poller = client.begin_analyze_document(
            "prebuilt-read", document_stream, content_type=request.content_type
        )
    else:
        raise ValueError("Either document_url or document_content and content_type must be provided.")

    result = poller.result()
    full_text = result.content if result.content else ""
    return ExtractedTextResult(text=full_text)
