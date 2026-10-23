from typing import Any, Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import create_client, open_document
from document_models import StructuredDocumentResponse, build_field


def extract_receipt_fields(document_path: str = None, document_bytes: bytes = None) -> StructuredDocumentResponse:
    client = create_client()
    document = open_document(document_path, document_bytes)
    poller = client.begin_analyze_document("prebuilt-receipt", AnalyzeDocumentRequest(bytes_source=document))
    result = poller.result()
    receipt = result.documents[0] if getattr(result, "documents", None) else None
    fields: Dict[str, Any] = {}
    if receipt and getattr(receipt, "fields", None):
        source = receipt.fields
        for key in ("MerchantName", "TotalTax", "Total", "Items"):
            if key in source:
                item = source[key]
                fields[key] = build_field(key, getattr(item, "value", None), getattr(item, "confidence", None), getattr(item, "page_number", None), getattr(item, "content", None))
    return StructuredDocumentResponse(provider="azure-document-intelligence-prebuilt-receipt", fields=fields, raw={"documents": getattr(result, "documents", None)})
