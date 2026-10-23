import boto3
from .document_client import get_client

def extract_layout(image_bytes):
    """Extract blocks, lines, tables, and other layout elements from a document image using Amazon Textract.
    """
    textract = get_client('textract')
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS', 'TABLES']
    )
    layout = {
        'lines': [],
        'tables': [],
        'fields': []
    }
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'LINE':
            layout['lines'].append(block['Text'])
        elif block['BlockType'] == 'CELL':
            layout['tables'].append(block)
        elif block['BlockType'] == 'KEY_VALUE_SET':
            layout['fields'].append(block)
    return layout
