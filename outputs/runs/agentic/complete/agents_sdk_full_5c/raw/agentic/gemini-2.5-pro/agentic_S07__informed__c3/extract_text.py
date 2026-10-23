from document_client import get_document_client

def extract_text_from_url(document_url: str) -> str:
    """
    Extracts plain text content from a document at a given URL.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        The extracted plain text content.
    """
    document_client = get_document_client()

    poller = document_client.begin_analyze_document(
        "prebuilt-read", {"urlSource": document_url}
    )
    result = poller.result()

    return result.content
