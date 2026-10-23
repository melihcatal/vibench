from document_client import get_azure_document_intelligence_client
from document_models import Invoice, InvoiceLineItem


def _get_field_value(doc, field_name):
    field = doc.fields.get(field_name)
    if field:
        return field.get("content")
    return None


def extract_invoice_fields(file_path: str) -> Invoice:
    client = get_azure_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream",
        )

    invoices = poller.result()
    invoice = invoices.documents[0] if invoices.documents else None

    if not invoice:
        raise Exception("No invoice found in document")

    vendor_name = _get_field_value(invoice, "VendorName")
    invoice_date = _get_field_value(invoice, "InvoiceDate")
    total_amount = _get_field_value(invoice, "InvoiceTotal")

    line_items = []
    items_field = invoice.fields.get("Items")
    if items_field and items_field.kind == "list":
        for item_doc in items_field.get("list", []):
            if item_doc.kind == "dictionary":
                description = _get_field_value(item_doc, "Description")
                quantity = _get_field_value(item_doc, "Quantity")
                unit_price = _get_field_value(item_doc, "UnitPrice")
                amount = _get_field_value(item_doc, "Amount")
                line_items.append(
                    InvoiceLineItem(
                        description=description,
                        quantity=quantity.get("number")
                        if isinstance(quantity, dict)
                        else quantity,
                        unit_price=unit_price.get("number")
                        if isinstance(unit_price, dict)
                        else unit_price,
                        amount=amount.get("number")
                        if isinstance(amount, dict)
                        else amount,
                    )
                )

    return Invoice(
        vendor_name=vendor_name,
        invoice_date=str(invoice_date) if invoice_date else None,
        total_amount=total_amount.get("number")
        if isinstance(total_amount, dict)
        else total_amount,
        line_items=line_items,
        raw_fields=invoice.fields,
    )
