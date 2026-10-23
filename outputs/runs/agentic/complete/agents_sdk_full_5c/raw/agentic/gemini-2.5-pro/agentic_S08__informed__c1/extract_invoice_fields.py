from document_client import get_document_intelligence_client
from document_models import Invoice, InvoiceLineItem

def extract_invoice_fields(file_path: str) -> Invoice:
    """
    Extracts structured data from an invoice document using Azure Document Intelligence.
    """
    document_intelligence_client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice", analyze_request=f, content_type="application/octet-stream"
        )
    invoices = poller.result()

    if not invoices.documents:
        raise ValueError("No invoice found in the document.")

    # Use the first document found
    doc = invoices.documents[0]
    
    vendor_name_field = doc.fields.get("VendorName")
    invoice_id_field = doc.fields.get("InvoiceId")
    invoice_date_field = doc.fields.get("InvoiceDate")
    invoice_total_field = doc.fields.get("InvoiceTotal")

    line_items = []
    items_field = doc.fields.get("Items")
    if items_field and items_field.kind == "list":
        for item_value in items_field.value:
            if item_value.kind == "dictionary":
                description = item_value.value.get("Description")
                quantity = item_value.value.get("Quantity")
                unit_price = item_value.value.get("UnitPrice")
                total = item_value.value.get("Amount")
                line_items.append(
                    InvoiceLineItem(
                        description=description.content if description else None,
                        quantity=quantity.value if quantity else None,
                        unit_price=unit_price.value if unit_price else None,
                        total_amount=total.value if total else None,
                    )
                )

    return Invoice(
        vendor_name=vendor_name_field.content if vendor_name_field else None,
        invoice_id=invoice_id_field.content if invoice_id_field else None,
        invoice_date=str(invoice_date_field.value) if invoice_date_field else None,
        invoice_total=invoice_total_field.value if invoice_total_field else None,
        line_items=line_items,
        raw_response=invoices.to_dict()
    )
