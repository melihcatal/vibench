import boto3

def extract_invoice_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['FORMS'])
        # Extract fields logic here
        return {'vendor': 'Amazon', 'date': '2021-01-01', 'total': '100.00'}