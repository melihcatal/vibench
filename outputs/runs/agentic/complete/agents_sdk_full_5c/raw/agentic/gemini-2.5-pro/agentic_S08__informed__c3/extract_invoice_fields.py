from document_client import get_document_client
from document_models import Invoice, LineItem

def extract_invoice(file_path: str) -> Invoice:
    """
    Extracts fields from an invoice document using Azure Document Intelligence.
    """
    client = get_document_client()
    
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", document=f)
    
    result = poller.result()
    invoice_data = Invoice()

    if result.documents:
        doc = result.documents[0]
        invoice_data.confidence = doc.confidence
        
        fields = doc.fields
        vendor_name_field = fields.get("VendorName")
        if vendor_name_field and vendor_name_field.value_string:
            invoice_data.vendor_name = vendor_name_field.value_string

        invoice_date_field = fields.get("InvoiceDate")
        if invoice_date_field and invoice_date_field.value_date:
            invoice_data.invoice_date = str(invoice_date_field.value_date)

        invoice_total_field = fields.get("InvoiceTotal")
        if invoice_total_field and invoice_total_field.value_amount:
            invoice_data.invoice_total = invoice_total_field.value_amount.amount

        items_field = fields.get("Items")
        if items_field and items_field.value_array:
            for item_value in items_field.value_array:
                if item_value.value_object:
                    item_fields = item_value.value_object
                    line_item = LineItem(
                        description=item_fields.get("Description", {}).get("value_string"),
                        quantity=item_fields.get("Quantity", {}).get("value_number"),
                        unit_price=item_fields.get("UnitPrice", {}).get("value_amount", {}).get("amount"),
                        total_price=item_fields.get("Amount", {}).get("value_amount", {}).get("amount"),
                    )
                    invoice_data.line_items.append(line_item)

    return invoice_data
