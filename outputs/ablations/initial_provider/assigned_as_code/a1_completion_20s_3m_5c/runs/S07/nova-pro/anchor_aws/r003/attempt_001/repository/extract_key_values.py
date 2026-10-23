import boto3
from document_client import get_textract_client

def extract_key_values(document_path):
    textract_client = get_textract_client()
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key_values[block['Text']] = None
            elif 'VALUE' in block['EntityTypes']:
                key_values[list(key_values.keys())[-1]] = block['Text']
    return key_values