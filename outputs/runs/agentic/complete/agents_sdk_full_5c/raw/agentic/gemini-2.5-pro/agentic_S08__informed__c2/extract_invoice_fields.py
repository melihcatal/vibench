
from document_client import get_document_intelligence_client
from azure.ai.documentintelligence.models import AnalyzeResult

def extract_invoice_fields_from_url(invoice_url: str) -> AnalyzeResult:
    """
    Extracts fields from an invoice document available at a URL.
    
    Args:
        invoice_url: The URL of the invoice document.

    Returns:
        An AnalyzeResult object from the Azure SDK.
    """
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document_from_url(
        "prebuilt-invoice", invoice_url
    )
    result = poller.result()
    return result

def extract_invoice_fields(invoice_bytes: bytes) -> AnalyzeResult:
    """
    Extracts fields from an invoice document provided as bytes.

    Args:
        invoice_bytes: The invoice document content in bytes.

    Returns:
        An AnalyzeResult object from the Azure SDK.
    """
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document(
        "prebuilt-invoice", invoice_bytes, content_type="application/octet-stream"
    )
    result = poller.result()
    return result
