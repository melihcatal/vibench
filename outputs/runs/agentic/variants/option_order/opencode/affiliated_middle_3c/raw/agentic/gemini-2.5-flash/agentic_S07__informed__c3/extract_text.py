from document_client import get_document_intelligence_client
from document_models import DocumentExtractionResult


def extract_text_from_document(
    document_content: bytes, mime_type: str
) -> DocumentExtractionResult:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-read", document_content, content_type=mime_type
    )
    result = poller.result()

    return DocumentExtractionResult(text_content=result.content)
