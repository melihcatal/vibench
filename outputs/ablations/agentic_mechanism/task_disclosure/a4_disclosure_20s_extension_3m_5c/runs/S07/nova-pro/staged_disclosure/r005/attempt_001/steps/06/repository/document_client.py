import boto3

def configure_textract_client(region_name='us-west-2'):
    return boto3.client('textract', region_name=region_name)

def extract_text(document_bytes):
    client = configure_textract_client()
    response = client.detect_document_text(Document={'Bytes': document_bytes})
    return response

def extract_layout(document_bytes):
    client = configure_textract_client()
    response = client.analyze_document(Document={'Bytes': document_bytes}, FeatureTypes=['TABLES', 'FORMS'])
    return response