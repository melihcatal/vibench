import boto3
from document_client import get_textract_client

def extract_layout(document_path):
    textract_client = get_textract_client()
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    layout = {
        'blocks': [],
        'lines': [],
        'tables': []
    }
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            layout['lines'].append(item['Text'])
        elif item['BlockType'] == 'TABLE':
            layout['tables'].append(item)
        elif item['BlockType'] == 'KEY_VALUE_SET':
            layout['blocks'].append(item)
    return layout