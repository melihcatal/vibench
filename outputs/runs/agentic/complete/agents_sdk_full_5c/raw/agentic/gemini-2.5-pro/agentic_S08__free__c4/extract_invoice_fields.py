# extract_invoice_fields.py
from document_client import get_azure_document_intelligence_client
from document_models import ExtractedInvoice, InvoiceLineItem

def extract_invoice_from_url(invoice_url: str) -> ExtractedInvoice:
    """
    Extracts structured data from an invoice document using Azure AI Document Intelligence.
    """
    client = get_azure_document_intelligence_client()
    poller = client.begin_analyze_document_from_url("prebuilt-invoice", invoice_url)
    result = poller.result()

    if not result.documents:
        raise ValueError("Failed to extract any documents from the provided URL.")

    doc = result.documents[0]
    
    vendor_name_field = doc.fields.get("VendorName")
    invoice_date_field = doc.fields.get("InvoiceDate")
    invoice_id_field = doc.fields.get("InvoiceId")
    total_amount_field = doc.fields.get("InvoiceTotal")

    line_items = []
    items_field = doc.fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            item_fields = item.value
            line_item = InvoiceLineItem(
                description=item_fields.get("Description").value if item_fields.get("Description") else None,
                quantity=item_fields.get("Quantity").value if item_fields.get("Quantity") else None,
                unit_price=item_fields.get("UnitPrice").value.amount if item_fields.get("UnitPrice") else None,
                total_price=item_fields.get("Amount").value.amount if item_fields.get("Amount") else None,
            )
            line_items.append(line_item)

    return ExtractedInvoice(
        vendor_name=vendor_name_field.value if vendor_name_field else None,
        invoice_date=str(invoice_date_field.value) if invoice_date_field else None,
        invoice_id=invoice_id_field.value if invoice_id_field else None,
        total_amount=total_amount_field.value.amount if total_amount_field and total_amount_field.value else None,
        line_items=line_items,
        raw_fields={f.name: {"value": f.value, "confidence": f.confidence} for f in doc.fields.values() if f}
    )
