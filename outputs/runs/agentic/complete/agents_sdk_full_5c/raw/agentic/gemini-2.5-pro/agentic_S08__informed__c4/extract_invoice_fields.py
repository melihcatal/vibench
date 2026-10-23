from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from document_client import get_document_client
import os

def extract_invoice_fields_from_url(invoice_url: str) -> AnalyzeResult:
    """
    Extracts fields from an invoice document at a given URL.
    
    :param invoice_url: The URL of the invoice document to analyze.
    :return: The AnalyzeResult object from the Azure Document Intelligence service.
    """
    doc_intelligence_client = get_document_client()
    
    poller = doc_intelligence_client.begin_analyze_document(
        "prebuilt-invoice",
        AnalyzeDocumentRequest(url_source=invoice_url)
    )
    result: AnalyzeResult = poller.result()
    return result

def extract_invoice_fields_from_file(file_path: str) -> AnalyzeResult:
    """
    Extracts fields from a local invoice document.

    :param file_path: The local path to the invoice document.
    :return: The AnalyzeResult object from the Azure Document Intelligence service.
    """
    doc_intelligence_client = get_document_client()
    
    with open(file_path, "rb") as f:
        poller = doc_intelligence_client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream"
        )
    result: AnalyzeResult = poller.result()
    return result
