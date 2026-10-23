from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_config, document_bytes


def extract_invoice_fields(document):
    cfg = ensure_config()
    client = DocumentIntelligenceClient(
        cfg.azure_endpoint, AzureKeyCredential(cfg.azure_key)
    )
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        AnalyzeDocumentRequest(bytes_source=document_bytes(document)),
    )
    result = poller.result()
    invoices = getattr(result, "documents", []) or []
    if not invoices:
        return {}
    invoice = invoices[0]
    fields = (
        invoice.get("fields", {})
        if isinstance(invoice, dict)
        else getattr(invoice, "fields", {})
    )
    return {
        "vendor": getattr(fields.get("VendorName"), "content", None)
        if hasattr(fields.get("VendorName"), "content")
        else None,
        "date": getattr(fields.get("InvoiceDate"), "content", None)
        if hasattr(fields.get("InvoiceDate"), "content")
        else None,
        "total": getattr(fields.get("InvoiceTotal"), "content", None)
        if hasattr(fields.get("InvoiceTotal"), "content")
        else None,
        "line_items": [],
    }
