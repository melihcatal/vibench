import json

def summarize_invoice_fields(extracted_fields):
    summary = {
        'vendor': extracted_fields.get('vendor', ''),
        'date': extracted_fields.get('date', ''),
        'total': extracted_fields.get('total', ''),
        'line_items': extracted_fields.get('line_items', [])
    }
    return json.dumps(summary, indent=2)