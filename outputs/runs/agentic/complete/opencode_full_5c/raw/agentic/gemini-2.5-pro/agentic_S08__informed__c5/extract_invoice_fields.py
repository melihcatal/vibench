from document_client import get_document_intelligence_client
from document_models import Invoice, LineItem


def extract_invoice_fields(file_path: str) -> Invoice:
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream",
        )

    invoices = poller.result()

    if not invoices.documents:
        return Invoice()

    doc = invoices.documents[0]

    vendor_name = doc.fields.get("VendorName")
    invoice_date = doc.fields.get("InvoiceDate")
    invoice_total = doc.fields.get("InvoiceTotal")

    extracted_line_items = []
    items = doc.fields.get("Items")
    if items and items.kind == "list":
        for item in items.value:
            if item.kind == "dictionary":
                description = item.value.get("Description")
                quantity = item.value.get("Quantity")
                unit_price = item.value.get("UnitPrice")
                total_price = item.value.get("Amount")

                extracted_line_items.append(
                    LineItem(
                        description=description.value if description else None,
                        quantity=quantity.value if quantity else None,
                        unit_price=unit_price.value if unit_price else None,
                        total_price=total_price.value if total_price else None,
                    )
                )

    return Invoice(
        vendor_name=vendor_name.value if vendor_name else None,
        invoice_date=str(invoice_date.value) if invoice_date else None,
        invoice_total=invoice_total.value if invoice_total else None,
        line_items=extracted_line_items,
    )
