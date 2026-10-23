from document_client import get_document_intelligence_client
from document_models import Invoice, InvoiceLineItem


def extract_invoice_fields_from_url(invoice_url: str) -> Invoice:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-invoice", analyze_request={"urlSource": invoice_url}
    )
    result = poller.result()

    invoice_data = {}
    line_items_data = []

    if result.documents:
        document = result.documents[0]
        invoice_data["raw_fields"] = {
            name: field.to_dict() for name, field in document.fields.items()
        }

        vendor_name = document.fields.get("VendorName")
        if vendor_name:
            invoice_data["vendor_name"] = vendor_name.get("content")

        invoice_date = document.fields.get("InvoiceDate")
        if invoice_date:
            invoice_data["invoice_date"] = str(invoice_date.get("value"))

        invoice_total = document.fields.get("InvoiceTotal")
        if invoice_total:
            invoice_data["invoice_total"] = (
                invoice_total.get("value").amount
                if invoice_total.get("value")
                else None
            )

        items = document.fields.get("Items")
        if items and items.get("value"):
            for item in items.get("value"):
                item_fields = item.get("value")
                line_item = InvoiceLineItem(
                    description=item_fields.get("Description").get("content")
                    if item_fields.get("Description")
                    else None,
                    quantity=item_fields.get("Quantity").get("value")
                    if item_fields.get("Quantity")
                    else None,
                    unit_price=item_fields.get("UnitPrice").get("value").amount
                    if item_fields.get("UnitPrice")
                    and item_fields.get("UnitPrice").get("value")
                    else None,
                    total_price=item_fields.get("Amount").get("value").amount
                    if item_fields.get("Amount")
                    and item_fields.get("Amount").get("value")
                    else None,
                )
                line_items_data.append(line_item)

    invoice_data["line_items"] = line_items_data
    return Invoice(**invoice_data)
