import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Any, List, Optional


def extract_invoice_fields(image_path: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream",
        )

    result = poller.result()

    vendor = None
    date = None
    total = None
    line_items = []

    for field_name, field in result.documents[0].fields.items():
        if field_name == "VendorName":
            vendor = field.value_string if field.value_string else None
        elif field_name == "InvoiceDate":
            date = field.value_date if field.value_date else None
        elif field_name == "InvoiceTotal":
            total = field.value_number if field.value_number else None
        elif field_name == "Items":
            if field.value_array:
                for item in field.value_array:
                    if item.value_object:
                        item_dict = {}
                        for item_field_name, item_field in item.value_object.items():
                            if item_field_name == "Description":
                                item_dict["description"] = item_field.value_string
                            elif item_field_name == "Quantity":
                                item_dict["quantity"] = item_field.value_number
                            elif item_field_name == "UnitPrice":
                                item_dict["unit_price"] = item_field.value_number
                            elif item_field_name == "Amount":
                                item_dict["amount"] = item_field.value_number
                        if item_dict:
                            line_items.append(item_dict)

    return {
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_items": line_items,
        "confidence": result.documents[0].confidence
        if hasattr(result.documents[0], "confidence")
        else None,
    }
