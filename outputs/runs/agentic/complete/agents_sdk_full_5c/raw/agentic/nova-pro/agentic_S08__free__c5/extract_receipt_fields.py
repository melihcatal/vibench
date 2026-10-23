import boto3

def extract_receipt_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES'])
    # Extract fields logic here