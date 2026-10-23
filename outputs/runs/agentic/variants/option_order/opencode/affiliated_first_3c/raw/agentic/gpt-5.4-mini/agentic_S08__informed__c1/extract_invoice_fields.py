from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_client_config, field_value_to_python


def extract_invoice_fields(document_url: str) -> Dict[str, Any]:
    config = load_document_client_config()
    client = DocumentIntelligenceClient(
        config.endpoint, AzureKeyCredential(config.api_key)
    )
    poller = client.begin_analyze_document(
        "prebuilt-invoice", analyze_request={"urlSource": document_url}
    )
    result = poller.result()
    invoice = (getattr(result, "documents", []) or [None])[0]
    fields = getattr(invoice, "fields", {}) if invoice else {}
    line_items = []
    for item in field_value_to_python(fields.get("Items")) or []:
        item_fields = getattr(item, "value", item)
        line_items.append(item_fields)
    return {
        "vendor": field_value_to_python(fields.get("VendorName")),
        "date": field_value_to_python(fields.get("InvoiceDate")),
        "total": field_value_to_python(fields.get("InvoiceTotal")),
        "line_items": line_items,
        "raw": result.to_dict() if hasattr(result, "to_dict") else {},
    }
