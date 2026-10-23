from mindee import InvoiceApi

MINDEE_API_KEY = 'your_mindee_api_key'
invoice_api = InvoiceApi(api_key=MINDEE_API_KEY)

def extract_receipt_fields(document):
    response = invoice_api.extract(document)
    # Extract fields from response
    return extracted_fields