import os
from typing import Dict, List, Any, Optional
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(invoice_path: str) -> Dict[str, Any]:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Form Recognizer credentials not configured")

    client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(invoice_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", document=f)

    result = poller.result()

    extracted_data = {"vendor": None, "date": None, "total": None, "line_items": []}

    for field_name, field in result.fields.items():
        if field_name == "VendorName" and field.value:
            extracted_data["vendor"] = field.value
        elif field_name == "InvoiceDate" and field.value:
            extracted_data["date"] = (
                field.value.isoformat()
                if hasattr(field.value, "isoformat")
                else str(field.value)
            )
        elif field_name == "InvoiceTotal" and field.value:
            extracted_data["total"] = float(field.value) if field.value else None

    if hasattr(result, "documents") and result.documents:
        for doc in result.documents:
            if hasattr(doc, "fields"):
                for field_name, field in doc.fields.items():
                    if field_name == "Items" and field.value:
                        for item in field.value:
                            if hasattr(item, "value"):
                                item_dict = {}
                                for item_field_name, item_field in item.value.items():
                                    if (
                                        item_field_name == "Description"
                                        and item_field.value
                                    ):
                                        item_dict["description"] = item_field.value
                                    elif (
                                        item_field_name == "Quantity"
                                        and item_field.value
                                    ):
                                        item_dict["quantity"] = float(item_field.value)
                                    elif (
                                        item_field_name == "UnitPrice"
                                        and item_field.value
                                    ):
                                        item_dict["unit_price"] = float(
                                            item_field.value
                                        )
                                    elif (
                                        item_field_name == "Amount" and item_field.value
                                    ):
                                        item_dict["amount"] = float(item_field.value)
                                if item_dict:
                                    extracted_data["line_items"].append(item_dict)

    return extracted_data
