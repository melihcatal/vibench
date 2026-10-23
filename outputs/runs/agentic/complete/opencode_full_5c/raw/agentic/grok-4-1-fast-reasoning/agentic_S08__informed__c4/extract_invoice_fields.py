import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import load_image


def extract_invoice_fields(image_path: str) -> dict:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT env var required")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY env var required")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = client.begin_analyze_document("prebuilt-invoice", load_image(image_path))
    result = poller.result()

    fields_dict = {}
    vendor_field = result.fields.get("VendorName")
    fields_dict["vendor"] = vendor_field.content if vendor_field else ""
    date_field = result.fields.get("InvoiceDate")
    fields_dict["date"] = date_field.content if date_field else ""
    total_field = result.fields.get("AmountDue") or result.fields.get("InvoiceTotal")
    fields_dict["total"] = (
        float(total_field.content) if total_field and total_field.content else 0.0
    )

    line_items = []
    if "LineItems" in result.fields and result.fields["LineItems"].values:
        for item in result.fields["LineItems"].values:
            li = {
                "description": item.get("Description", {}).content or "",
                "amount": float(item.get("Amount", {}).content or 0),
            }
            line_items.append(li)
    fields_dict["line_items"] = line_items

    conf = {}
    for k, v in result.fields.items():
        if hasattr(v, "confidence"):
            conf[k] = v.confidence
    fields_dict["confidence"] = conf

    return fields_dict
