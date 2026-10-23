from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_config, document_bytes


def extract_receipt_fields(document):
    cfg = ensure_config()
    client = DocumentIntelligenceClient(
        cfg.azure_endpoint, AzureKeyCredential(cfg.azure_key)
    )
    poller = client.begin_analyze_document(
        "prebuilt-receipt",
        AnalyzeDocumentRequest(bytes_source=document_bytes(document)),
    )
    result = poller.result()
    receipts = getattr(result, "documents", []) or []
    if not receipts:
        return {}
    receipt = receipts[0]
    fields = (
        receipt.get("fields", {})
        if isinstance(receipt, dict)
        else getattr(receipt, "fields", {})
    )
    return {
        "merchant": getattr(fields.get("MerchantName"), "content", None)
        if hasattr(fields.get("MerchantName"), "content")
        else None,
        "tax": getattr(fields.get("Tax"), "content", None)
        if hasattr(fields.get("Tax"), "content")
        else None,
        "total": getattr(fields.get("Total"), "content", None)
        if hasattr(fields.get("Total"), "content")
        else None,
        "items": [],
    }
