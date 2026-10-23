import mindee

api_key = os.getenv('MINDEE_API_KEY')
client = mindee.Client(api_key)

def extract_receipt_fields(document_path):
    receipt_document = client.receipts.parse(document_path)
    return receipt_document