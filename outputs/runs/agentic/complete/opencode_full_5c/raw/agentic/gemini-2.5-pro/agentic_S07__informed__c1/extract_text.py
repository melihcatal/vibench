from document_client import get_document_client
from document_models import DocumentTextBlock


def extract_text_from_document(file_path: str) -> DocumentTextBlock:
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", analyze_request=f, content_type="application/octet-stream"
        )
    result = poller.result()

    full_text = ""
    page_number = 1
    if result.pages:
        page_number = result.pages[0].page_number

    if result.content:
        full_text = result.content

    return DocumentTextBlock(content=full_text, page_number=page_number)
