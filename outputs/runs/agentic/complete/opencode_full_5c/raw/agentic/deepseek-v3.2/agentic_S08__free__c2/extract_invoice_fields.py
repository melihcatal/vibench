import os
import json
from typing import Dict, Any, List, Optional
import requests
from document_client import get_azure_form_recognizer_client
from document_models import InvoiceExtractionRequest, InvoiceExtractionResult


def extract_invoice_fields(
    image_path: str, invoice_type: str = "standard"
) -> InvoiceExtractionResult:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Azure Form Recognizer.
    """
    try:
        client = get_azure_form_recognizer_client()

        with open(image_path, "rb") as f:
            image_data = f.read()

        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice", document=image_data
        )
        result = poller.result()

        extracted_fields = {}
        line_items = []

        for document in result.documents:
            for field_name, field in document.fields.items():
                if field.value:
                    extracted_fields[field_name] = {
                        "value": field.value,
                        "confidence": field.confidence,
                    }

            if "Items" in document.fields and document.fields["Items"].value:
                for item in document.fields["Items"].value:
                    item_dict = {}
                    for item_field_name, item_field in item.value.items():
                        if item_field.value:
                            item_dict[item_field_name] = {
                                "value": item_field.value,
                                "confidence": item_field.confidence,
                            }
                    if item_dict:
                        line_items.append(item_dict)

        vendor = extracted_fields.get("VendorName", {}).get("value", "")
        invoice_date = extracted_fields.get("InvoiceDate", {}).get("value", "")
        total = extracted_fields.get("InvoiceTotal", {}).get("value", "")

        return InvoiceExtractionResult(
            vendor=vendor,
            invoice_date=str(invoice_date) if invoice_date else "",
            total_amount=str(total) if total else "",
            line_items=line_items,
            raw_fields=extracted_fields,
            confidence_scores={
                "vendor": extracted_fields.get("VendorName", {}).get("confidence", 0.0),
                "date": extracted_fields.get("InvoiceDate", {}).get("confidence", 0.0),
                "total": extracted_fields.get("InvoiceTotal", {}).get(
                    "confidence", 0.0
                ),
            },
            provider="azure_form_recognizer",
            model_used="prebuilt-invoice",
        )

    except Exception as e:
        raise Exception(f"Azure Form Recognizer extraction failed: {str(e)}")
