from mindee import InvoiceApi

def normalize_expense(document_path):
    api = InvoiceApi()
    with open(document_path, 'rb') as document:
        response = api.extract(document)
    return response