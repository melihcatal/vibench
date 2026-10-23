import os
import json
from typing import Dict, List, Any, Optional
from document_client import get_document_client
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Azure Form Recognizer.
    """
    client = get_document_client()

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    # Use Azure Form Recognizer prebuilt-invoice model
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice", document=file_bytes
    )

    result = poller.result()

    extracted_data = {"vendor": None, "date": None, "total": None, "line_items": []}

    # Extract vendor information
    for document in result.documents:
        if "VendorName" in document.fields:
            extracted_data["vendor"] = document.fields["VendorName"].value

        if "InvoiceDate" in document.fields:
            extracted_data["date"] = document.fields["InvoiceDate"].value

        if "InvoiceTotal" in document.fields:
            extracted_data["total"] = document.fields["InvoiceTotal"].value

        # Extract line items
        if "Items" in document.fields:
            items = document.fields["Items"].value
            if items:
                for item in items:
                    line_item = {}
                    if "Description" in item.value:
                        line_item["description"] = item.value["Description"].value
                    if "Amount" in item.value:
                        line_item["amount"] = item.value["Amount"].value
                    if "Quantity" in item.value:
                        line_item["quantity"] = item.value["Quantity"].value
                    if "UnitPrice" in item.value:
                        line_item["unit_price"] = item.value["UnitPrice"].value

                    extracted_data["line_items"].append(line_item)

    return extracted_data


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        result = extract_invoice_fields(sys.argv[1])
        print(json.dumps(result, indent=2, default=str))
