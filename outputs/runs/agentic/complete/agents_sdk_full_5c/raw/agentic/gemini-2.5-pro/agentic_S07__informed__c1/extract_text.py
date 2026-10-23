from document_client import get_document_client
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import Optional

def extract_text_from_url(document_url: str) -> Optional[str]:
    """
    Extracts plain text from a document at a given URL using Azure Document Intelligence.
    
    Args:
        document_url: The URL of the document to analyze.
        
    Returns:
        The extracted plain text content, or None if analysis fails.
    """
    client = get_document_client()
    
    poller = client.begin_analyze_document_from_url(
        model_id="prebuilt-read",
        url=document_url
    )
    result: AnalyzeResult = poller.result()
    
    if result.content:
        return result.content
    return None

def extract_text_from_file(document_path: str) -> Optional[str]:
    """
    Extracts plain text from a local document file using Azure Document Intelligence.
    
    Args:
        document_path: The local path to the document file.
        
    Returns:
        The extracted plain text content, or None if analysis fails.
    """
    client = get_document_client()
    
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            document=f.read()
        )
    result: AnalyzeResult = poller.result()
    
    if result.content:
        return result.content
    return None
