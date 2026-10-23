import boto3

def summarize_invoice_fields(extracted_fields):
    invoice_summary = {
        'vendor': extracted_fields.get('vendor', ''),
        'date': extracted_fields.get('date', ''),
        'total': extracted_fields.get('total', ''),
        'line_items': extracted_fields.get('line_items', [])
    }
    return invoice_summary