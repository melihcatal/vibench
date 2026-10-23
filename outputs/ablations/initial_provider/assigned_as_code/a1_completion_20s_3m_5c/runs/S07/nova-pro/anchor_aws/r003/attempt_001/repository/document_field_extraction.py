import boto3
from document_client import get_textract_client

def document_field_extraction(document_path):
    textract_client = get_textract_client()
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                fields[block['Text']] = None
            elif 'VALUE' in block['EntityTypes']:
                fields[list(fields.keys())[-1]] = block['Text']
    return fields