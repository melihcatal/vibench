from document_client import get_document_client
from document_models import Invoice, LineItem


def extract_invoice(file_path: str) -> Invoice:
    """
    Extracts fields from an invoice document using Azure Document Intelligence.
    """
    client = get_document_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream",
        )

    invoices = poller.result()

    if not invoices.documents:
        return Invoice()

    # Assuming the first document is the main invoice
    doc = invoices.documents[0]

    vendor_name = doc.fields.get("VendorName")
    vendor_address = doc.fields.get("VendorAddress")
    customer_name = doc.fields.get("CustomerName")
    customer_address = doc.fields.get("CustomerAddress")
    invoice_id = doc.fields.get("InvoiceId")
    invoice_date = doc.fields.get("InvoiceDate")
    due_date = doc.fields.get("DueDate")
    total_amount = doc.fields.get("InvoiceTotal")
    total_tax = doc.fields.get("TotalTax")

    extracted_invoice = Invoice(
        vendor_name=vendor_name.value if vendor_name else None,
        vendor_address=vendor_address.content if vendor_address else None,
        customer_name=customer_name.value if customer_name else None,
        customer_address=customer_address.content if customer_address else None,
        invoice_id=invoice_id.value if invoice_id else None,
        invoice_date=str(invoice_date.value) if invoice_date else None,
        due_date=str(due_date.value) if due_date else None,
        total_amount=total_amount.value.amount
        if total_amount and total_amount.value
        else None,
        total_tax=total_tax.value.amount if total_tax and total_tax.value else None,
        raw_document=doc.to_dict(),
    )

    items_field = doc.fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            line_item = LineItem(
                description=item.value.get("Description", {}).get("content"),
                quantity=item.value.get("Quantity", {}).get("value"),
                unit_price=item.value.get("UnitPrice", {})
                .get("value", {})
                .get("amount"),
                total_price=item.value.get("Amount", {}).get("value", {}).get("amount"),
            )
            extracted_invoice.line_items.append(line_item)

    return extracted_invoice
