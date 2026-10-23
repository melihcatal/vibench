# Request and response models for Structured Document Extraction

def build_invoice_request(file_bytes):
    '''Prepare payload for an invoice extraction call.'''
    # Example structure for Mindee SDK - adapt as needed
    return {'file': file_bytes}

def parse_invoice_response(raw_response):
    '''Extract useful fields from raw invoice response.'''
    # Stub: adapt to specific provider SDK response format
    return {'vendor': None, 'date': None, 'total': None, 'line_items': []}

# Similar helpers can be added for receipts, translations, etc.
