from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from document_client import get_document_client

def extract_text_from_url(document_url: str) -> str:
    """
    Extracts plain text from a document image using Azure AI Document Intelligence.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        The concatenated text content from the document.
    """
    client = get_document_client()

    poller = client.begin_analyze_document(
        "prebuilt-read", AnalyzeDocumentRequest(url_source=document_url)
    )
    result = poller.result()

    if result.content:
        return result.content
    return ""
