"""
Extracts vendor, date, total, and line-item fields from an invoice
using Azure Document Intelligence.
"""
from document_client import get_azure_document_intelligence_client
from document_models import Invoice, LineItem

def extract_invoice(file_path: str) -> Invoice:
    """
    Extracts structured data from an invoice document.
    """
    document_intelligence_client = get_azure_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice", analyze_request=f, content_type="application/octet-stream"
        )
    invoices = poller.result()

    if not invoices.documents:
        return Invoice(vendor_name=None, invoice_date=None, invoice_total=None)

    # Assuming one invoice per document for simplicity
    extracted_invoice = invoices.documents[0]
    
    vendor_name_field = extracted_invoice.fields.get("VendorName")
    invoice_date_field = extracted_invoice.fields.get("InvoiceDate")
    invoice_total_field = extracted_invoice.fields.get("InvoiceTotal")

    items = []
    items_field = extracted_invoice.fields.get("Items")
    if items_field and items_field.value_array:
        for item_fields in items_field.value_array:
            if item_fields.value_object:
                description = item_fields.value_object.get("Description")
                quantity = item_fields.value_object.get("Quantity")
                unit_price = item_fields.value_object.get("UnitPrice")
                total = item_fields.value_object.get("Amount")
                items.append(
                    LineItem(
                        description=description.content if description else None,
                        quantity=quantity.value_number if quantity else None,
                        unit_price=unit_price.value_amount.amount if unit_price else None,
                        total_amount=total.value_amount.amount if total else None,
                    )
                )

    return Invoice(
        vendor_name=vendor_name_field.content if vendor_name_field else None,
        invoice_date=str(invoice_date_field.value_date) if invoice_date_field else None,
        invoice_total=invoice_total_field.value_amount.amount if invoice_total_field else None,
        items=items,
    )
