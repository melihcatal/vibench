import os
from document_client import get_azure_document_intelligence_client


def extract_invoice_fields(invoice_document_path: str) -> dict:
    client = get_azure_document_intelligence_client()

    with open(invoice_document_path, "rb") as f:
        poller = client.begin_analyze_document(
            document_model_id="prebuilt-invoice", document=f
        )
        result = poller.result()

    extracted_fields = {
        "vendor_name": result.documents[0].fields.get("VendorName").content
        if result.documents[0].fields.get("VendorName")
        else None,
        "transaction_date": result.documents[0].fields.get("InvoiceDate").value
        if result.documents[0].fields.get("InvoiceDate")
        else None,
        "total_amount": result.documents[0].fields.get("InvoiceTotal").value
        if result.documents[0].fields.get("InvoiceTotal")
        else None,
        "currency": result.documents[0].fields.get("InvoiceTotal").currency_symbol
        if result.documents[0].fields.get("InvoiceTotal")
        else None,
        "line_items": [],
    }

    if result.documents[0].fields.get("Items"):
        for item in result.documents[0].fields.get("Items").value:
            extracted_fields["line_items"].append(
                {
                    "description": item.value.get("Description").content
                    if item.value.get("Description")
                    else None,
                    "quantity": item.value.get("Quantity").value
                    if item.value.get("Quantity")
                    else None,
                    "unit_price": item.value.get("UnitPrice").value
                    if item.value.get("UnitPrice")
                    else None,
                    "total_price": item.value.get("Amount").value
                    if item.value.get("Amount")
                    else None,
                }
            )

    return extracted_fields
