from document_client import get_document_client


def extract_text_from_url(document_url: str) -> str:
    """
    Extracts plain text from a document at a given URL.
    Uses Azure AI Document Intelligence's "prebuilt-read" model.
    """
    document_analysis_client = get_document_client()

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-read", document_url
    )
    result = poller.result()

    return result.content
