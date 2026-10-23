from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import get_document_intelligence_client
from document_models import ExtractedText

def extract_text_from_url(url: str) -> ExtractedText:
    """
    Extracts plain text from a document at a given URL using Azure Document Intelligence.

    Args:
        url: The URL of the document to analyze.

    Returns:
        An ExtractedText object containing the full text content.
    """
    document_intelligence_client = get_document_intelligence_client()
    
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", {"urlSource": url}
    )
    result = poller.result()

    return ExtractedText(content=result.content)

def extract_text_from_file(file_path: str) -> ExtractedText:
    """
    Extracts plain text from a local document file.

    Args:
        file_path: The path to the local document file.

    Returns:
        An ExtractedText object containing the full text content.
    """
    document_intelligence_client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", f, content_type="application/octet-stream"
        )
    result = poller.result()
    
    return ExtractedText(content=result.content)
