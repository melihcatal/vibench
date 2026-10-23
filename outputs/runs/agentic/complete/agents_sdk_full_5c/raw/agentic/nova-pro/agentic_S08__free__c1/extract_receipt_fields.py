import boto3

def extract_receipt_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['TABLES'])
        # Extract fields logic here
        return {'merchant': 'Amazon', 'tax': '10.00', 'total': '110.00'}