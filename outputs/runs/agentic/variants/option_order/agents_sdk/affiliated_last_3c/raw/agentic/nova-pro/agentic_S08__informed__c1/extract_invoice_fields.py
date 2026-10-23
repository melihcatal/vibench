import mindee

api_key = os.getenv('MINDEE_API_KEY')
client = mindee.Client(api_key)

def extract_invoice_fields(document_path):
    invoice_document = client.invoices.parse(document_path)
    return invoice_document