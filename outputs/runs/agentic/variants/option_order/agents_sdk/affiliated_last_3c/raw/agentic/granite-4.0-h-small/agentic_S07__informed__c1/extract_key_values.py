import boto3
from .document_client import get_client

def extract_key_values(image_bytes):
    """Extract key-value pairs from a form-like document using Amazon Textract.
    """
    textract = get_client('textract')
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    key_values = {}
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'KEY_VALUE_SET':
            key = next((k['Text'] for k in item.get('Relationships', []) if k['Type'] == 'KEY'), None)
            value = next((v['Text'] for v in item.get('Relationships', []) if v['Type'] == 'VALUE'), None)
            if key and value:
                key_values[key] = value
    return key_values
