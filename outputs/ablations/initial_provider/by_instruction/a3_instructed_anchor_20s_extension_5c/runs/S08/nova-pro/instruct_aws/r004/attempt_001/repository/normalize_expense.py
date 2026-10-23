def normalize_expense(extracted_fields):
    normalized_expense = {
        'vendor': extracted_fields.get('Vendor', ''),
        'date': extracted_fields.get('Date', ''),
        'total': extracted_fields.get('Total', ''),
        'line_items': extracted_fields.get('Line Items', [])
    }
    return normalized_expense