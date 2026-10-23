import mindee

def extract_receipt_fields(document):
    client = mindee.Client(api_key=os.getenv('MINDEE_API_KEY'))
    receipt = client.documents.create(document)
    # Extract fields from receipt
    return {'merchant': 'extracted_merchant', 'tax': 'extracted_tax', 'total': 'extracted_total', 'items': 'extracted_items'}