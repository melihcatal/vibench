def summarize_invoice_fields(extracted_fields):
    summary = f"Invoice from {extracted_fields['vendor']} on {extracted_fields['date']} for a total of {extracted_fields['total']}"
    return summary