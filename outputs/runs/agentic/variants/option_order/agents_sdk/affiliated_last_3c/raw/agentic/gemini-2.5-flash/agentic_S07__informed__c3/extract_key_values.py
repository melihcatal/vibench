from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValueResult, DocumentProcessingRequest
import io

def extract_key_value_pairs(request: DocumentProcessingRequest) -> ExtractedKeyValueResult:
    """
    Extracts key-value pairs from a form-like document using Azure Document Intelligence.
    Uses the prebuilt-document model which is capable of extracting key-value pairs.
    """
    client = get_document_intelligence_client()

    if request.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-document", document_url=request.document_url
        )
    elif request.document_content and request.content_type:
        document_stream = io.BytesIO(request.document_content)
        poller = client.begin_analyze_document(
            "prebuilt-document", document_stream, content_type=request.content_type
        )
    else:
        raise ValueError("Either document_url or document_content and content_type must be provided.")

    result = poller.result()

    key_value_pairs = {}
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            if kvp.key and kvp.value:
                key_value_pairs[kvp.key.content] = kvp.value.content

    return ExtractedKeyValueResult(key_values=key_value_pairs)
