from document_client import get_document_intelligence_client


def extract_text_from_document(file_path: str) -> str:
    """
    Extracts plain text from a document image.
    """
    document_intelligence_client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", analyze_request=f, content_type="application/octet-stream"
        )
    result = poller.result()
    return result.content
