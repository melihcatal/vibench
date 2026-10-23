import boto3

def extract_key_values(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['FORMS'])
    key_values = response['Blocks']
    return key_values