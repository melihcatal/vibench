import os
from document_client import get_document_intelligence_client
from document_models import ExpenseDocument, LineItem

def extract_invoice_fields(document_url: str) -> ExpenseDocument:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document_from_url(
        "prebuilt-invoice", document_url
    )
    invoice_result = poller.result()

    vendor_name = None
    if invoice_result.documents and invoice_result.documents[0].fields.get("VendorName"):
        vendor_name = invoice_result.documents[0].fields.get("VendorName").value

    date = None
    if invoice_result.documents and invoice_result.documents[0].fields.get("InvoiceDate"):
        date = str(invoice_result.documents[0].fields.get("InvoiceDate").value)

    total_amount = None
    if invoice_result.documents and invoice_result.documents[0].fields.get("InvoiceTotal"):
        total_amount = invoice_result.documents[0].fields.get("InvoiceTotal").value

    currency = None
    if invoice_result.documents and invoice_result.documents[0].fields.get("InvoiceTotal") and invoice_result.documents[0].fields.get("InvoiceTotal").currency_symbol:
        currency = invoice_result.documents[0].fields.get("InvoiceTotal").currency_symbol

    invoice_number = None
    if invoice_result.documents and invoice_result.documents[0].fields.get("InvoiceId"):
        invoice_number = invoice_result.documents[0].fields.get("InvoiceId").value

    line_items = []
    if invoice_result.documents and invoice_result.documents[0].fields.get("Items"):
        for item in invoice_result.documents[0].fields.get("Items").value:
            description = item.value.get("Description").value if item.value.get("Description") else None
            quantity = item.value.get("Quantity").value if item.value.get("Quantity") else None
            unit_price = item.value.get("UnitPrice").value if item.value.get("UnitPrice") else None
            amount = item.value.get("Amount").value if item.value.get("Amount") else None
            line_items.append(LineItem(description=description, quantity=quantity, unit_price=unit_price, amount=amount))

    return ExpenseDocument(
        document_type="invoice",
        vendor_name=vendor_name,
        date=date,
        total_amount=total_amount,
        currency=currency,
        invoice_number=invoice_number,
        line_items=line_items,
        raw_response=invoice_result.to_dict()
    )
