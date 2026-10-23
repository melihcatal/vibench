import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_expense(Document={'Bytes': document.read()})
    return response