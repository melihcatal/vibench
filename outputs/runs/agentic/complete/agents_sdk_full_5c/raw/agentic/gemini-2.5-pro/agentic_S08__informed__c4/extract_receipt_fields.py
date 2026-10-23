from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from document_client import get_document_client

def extract_receipt_fields_from_url(receipt_url: str) -> AnalyzeResult:
    """
    Extracts fields from a receipt document at a given URL.
    
    :param receipt_url: The URL of the receipt to analyze.
    :return: The AnalyzeResult object from the Azure Document Intelligence service.
    """
    doc_intelligence_client = get_document_client()
    
    poller = doc_intelligence_client.begin_analyze_document(
        "prebuilt-receipt",
        AnalyzeDocumentRequest(url_source=receipt_url)
    )
    result: AnalyzeResult = poller.result()
    return result

def extract_receipt_fields_from_file(file_path: str) -> AnalyzeResult:
    """
    Extracts fields from a local receipt document.

    :param file_path: The local path to the receipt document.
    :return: The AnalyzeResult object from the Azure Document Intelligence service.
    """
    doc_intelligence_client = get_document_client()
    
    with open(file_path, "rb") as f:
        poller = doc_intelligence_client.begin_analyze_document(
            "prebuilt-receipt",
            analyze_request=f,
            content_type="application/octet-stream"
        )
    result: AnalyzeResult = poller.result()
    return result
