# extract_invoice_fields.py
from document_client import get_azure_document_intelligence_client
from document_models import ExtractedInvoice, ExtractedLineItem

def extract_invoice_fields_from_url(invoice_url: str) -> ExtractedInvoice:
    """
    Extracts fields from an invoice document at a given URL using Azure AI Document Intelligence.
    """
    document_intelligence_client = get_azure_document_intelligence_client()

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-invoice", analyze_request={"urlSource": invoice_url}
    )
    result = poller.result()

    invoice = result.documents[0] if result.documents else None
    if not invoice:
        raise ValueError("Failed to extract any document from the provided URL.")

    vendor_name = invoice.fields.get("VendorName")
    invoice_date = invoice.fields.get("InvoiceDate")
    total_amount = invoice.fields.get("InvoiceTotal")

    extracted_line_items = []
    items_field = invoice.fields.get("Items")
    if items_field and items_field.value_array:
        for item_value in items_field.value_array:
            item_fields = item_value.value_object
            description = item_fields.get("Description")
            quantity = item_fields.get("Quantity")
            unit_price = item_fields.get("UnitPrice")
            total = item_fields.get("Amount")
            
            extracted_line_items.append(ExtractedLineItem(
                description=description.value if description else None,
                quantity=quantity.value if quantity else None,
                unit_price=unit_price.value if unit_price else None,
                total_amount=total.value if total else None,
            ))

    return ExtractedInvoice(
        vendor_name=vendor_name.value if vendor_name else None,
        invoice_date=str(invoice_date.value) if invoice_date else None,
        total_amount=total_amount.value if total_amount else None,
        line_items=extracted_line_items,
        raw_fields={f.key: f.value for f in invoice.fields.values() if f.value is not None}
    )
