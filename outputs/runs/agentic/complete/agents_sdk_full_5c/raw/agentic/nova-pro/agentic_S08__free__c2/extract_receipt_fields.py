import boto3

client = boto3.client('textract')

def extract_receipt_fields(document):
    response = client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    # Extract fields logic here
    return {}