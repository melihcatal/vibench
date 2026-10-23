def summarize_invoice_fields(extracted_fields):
    summary = f"Vendor: {extracted_fields.get('vendor', '')}, Date: {extracted_fields.get('date', '')}, Total: {extracted_fields.get('total', '')}"
    return summary