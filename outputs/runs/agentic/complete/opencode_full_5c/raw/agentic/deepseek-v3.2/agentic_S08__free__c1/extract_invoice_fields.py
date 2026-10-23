import os
from typing import Dict, List, Any
import json
from document_client import get_document_client
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse


def extract_invoice_fields(invoice_image_path: str) -> Dict[str, Any]:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Azure Form Recognizer.
    """
    client = get_document_client()

    with open(invoice_image_path, "rb") as f:
        invoice_bytes = f.read()

    request = InvoiceExtractionRequest(
        document_bytes=invoice_bytes, document_type="invoice"
    )

    # Use Azure Form Recognizer prebuilt invoice model
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", invoice_bytes
    )
    result = poller.result()

    extracted_fields = {}

    # Extract vendor information
    vendor_name = None
    vendor_address = None
    vendor_tax_id = None

    for field_name, field in result.fields.items():
        if field_name == "VendorName" and field.value:
            vendor_name = field.value
        elif field_name == "VendorAddress" and field.value:
            vendor_address = field.value
        elif field_name == "VendorTaxId" and field.value:
            vendor_tax_id = field.value

    # Extract date
    invoice_date = None
    if "InvoiceDate" in result.fields and result.fields["InvoiceDate"].value:
        invoice_date = result.fields["InvoiceDate"].value.isoformat()

    # Extract total
    invoice_total = None
    if "InvoiceTotal" in result.fields and result.fields["InvoiceTotal"].value:
        invoice_total = float(result.fields["InvoiceTotal"].value.amount)

    # Extract line items
    line_items = []
    if "Items" in result.fields and result.fields["Items"].value:
        for item in result.fields["Items"].value:
            item_dict = {}
            for item_field_name, item_field in item.value.items():
                if item_field.value:
                    if item_field_name in ["Description", "ProductCode"]:
                        item_dict[item_field_name] = str(item_field.value)
                    elif item_field_name in ["Quantity", "UnitPrice", "Amount"]:
                        if hasattr(item_field.value, "amount"):
                            item_dict[item_field_name] = float(item_field.value.amount)
                        else:
                            item_dict[item_field_name] = float(item_field.value)
            if item_dict:
                line_items.append(item_dict)

    extracted_fields = {
        "vendor": {
            "name": vendor_name,
            "address": vendor_address,
            "tax_id": vendor_tax_id,
        },
        "date": invoice_date,
        "total": invoice_total,
        "line_items": line_items,
        "confidence": result.api_version,
        "provider": "azure_form_recognizer",
        "model": "prebuilt-invoice",
    }

    return extracted_fields
