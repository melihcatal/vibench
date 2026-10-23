import boto3

def validate_document_fields(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['FORMS'])
    return response