import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Provider-specific credentials
ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
CLIENT = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))
MODEL_ID = "prebuilt-invoice"  # Azure prebuilt invoice model identifier

def extract_invoice_fields(document_bytes):
    """Extract vendor, date, total, and line items from an invoice using Azure Document Intelligence."""
    poller = CLIENT.begin_analyze_document(model_id=MODEL_ID, document=document_bytes)
    result = poller.result()
    fields = {}
    for field in result.fields:
        name = field.name.lower()
        if name in ("vendor", "date", "total"):
            fields[name] = field.value
        elif name == "item":
            # Collect line items
            items = []
            for item_field in field.items:
                items.append({
                    "description": item_field.item_description,
                    "qty": item_field.item_quantity,
                    "unit_price": item_field.item_unit_price,
                    "total": item_field.item_total
                })
            fields["items"] = items
    return fields
