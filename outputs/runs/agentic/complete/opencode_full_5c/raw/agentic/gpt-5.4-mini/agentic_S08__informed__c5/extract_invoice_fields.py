from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_service_config
from document_models import StructuredDocumentResponse, normalize_money


def extract_invoice_fields(document_bytes: bytes) -> dict:
    config = load_service_config("AZURE_DOCUMENT_INTELLIGENCE")
    client = DocumentIntelligenceClient(
        config.endpoint, AzureKeyCredential(config.api_key)
    )
    poller = client.begin_analyze_document("prebuilt-invoice", document=document_bytes)
    result = poller.result()
    fields = result.documents[0].fields if result.documents else {}
    line_items = []
    for item in fields.get("Items", {}).get("value_array", []) or []:
        item_fields = item.value_object or {}
        line_items.append(
            {
                "description": getattr(item_fields.get("Description"), "content", None),
                "quantity": getattr(item_fields.get("Quantity"), "value", None),
                "amount": normalize_money(
                    getattr(item_fields.get("Amount"), "content", None)
                ),
            }
        )
    response = StructuredDocumentResponse(
        document_type="invoice",
        fields={
            "vendor": getattr(fields.get("VendorName"), "content", None),
            "date": getattr(fields.get("InvoiceDate"), "content", None),
            "total": normalize_money(
                getattr(fields.get("InvoiceTotal"), "content", None)
            ),
            "line_items": line_items,
        },
        raw={"service": "azure-ai-documentintelligence"},
    )
    return response.__dict__
