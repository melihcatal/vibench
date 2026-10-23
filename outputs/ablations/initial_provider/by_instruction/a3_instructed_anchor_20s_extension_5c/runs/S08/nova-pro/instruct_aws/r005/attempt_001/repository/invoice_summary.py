import boto3

def summarize_invoice_fields(invoice):
    summarized_invoice = {
        'vendor': invoice.get('vendor', ''),
        'date': invoice.get('date', ''),
        'total': invoice.get('total', ''),
        'line_items': invoice.get('line_items', [])
    }
    return summarized_invoice