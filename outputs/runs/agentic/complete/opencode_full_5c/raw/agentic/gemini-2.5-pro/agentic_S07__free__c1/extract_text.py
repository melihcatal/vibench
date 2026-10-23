from document_client import get_document_intelligence_client


def extract_text(image_path: str) -> str:
    """
    Extracts plain text from a document image.
    """
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    return result.content
