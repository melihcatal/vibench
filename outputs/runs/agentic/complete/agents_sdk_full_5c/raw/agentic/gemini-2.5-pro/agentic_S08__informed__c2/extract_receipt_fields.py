
from document_client import get_document_intelligence_client
from azure.ai.documentintelligence.models import AnalyzeResult

def extract_receipt_fields_from_url(receipt_url: str) -> AnalyzeResult:
    """
    Extracts fields from a receipt document available at a URL.
    
    Args:
        receipt_url: The URL of the receipt document.

    Returns:
        An AnalyzeResult object from the Azure SDK.
    """
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document_from_url(
        "prebuilt-receipt", receipt_url
    )
    result = poller.result()
    return result


def extract_receipt_fields(receipt_bytes: bytes) -> AnalyzeResult:
    """
    Extracts fields from a receipt document provided as bytes.

    Args:
        receipt_bytes: The receipt document content in bytes.

    Returns:
        An AnalyzeResult object from the Azure SDK.
    """
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document(
        "prebuilt-receipt", receipt_bytes, content_type="application/octet-stream"
    )
    result = poller.result()
    return result
