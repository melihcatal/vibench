import boto3

def configure_client(region_name='us-west-2'):
    return boto3.client('textract', region_name=region_name)

def extract_text(document_path, client):
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = client.detect_document_text(Document={'Bytes': image_bytes})
    return response

def extract_layout(document_path, client):
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['TABLES', 'FORMS'])
    return response