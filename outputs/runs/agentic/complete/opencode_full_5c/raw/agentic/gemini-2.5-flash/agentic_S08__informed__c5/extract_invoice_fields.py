from document_client import get_azure_document_intelligence_client
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_invoice_fields_azure_di(document_content: bytes) -> AnalyzeResult:
    document_intelligence_client = get_azure_document_intelligence_client()
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-invoice", document_content, content_type="application/octet-stream"
    )
    invoice_result: AnalyzeResult = poller.result()
    return invoice_result
