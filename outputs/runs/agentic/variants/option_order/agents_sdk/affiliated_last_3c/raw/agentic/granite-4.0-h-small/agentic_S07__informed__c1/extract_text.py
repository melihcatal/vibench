import boto3
from .document_client import get_client

def extract_text(image_bytes):
    """Extract plain text from a scanned document image using Amazon Textract.
    """
    textract = get_client('textract')
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    text = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            text.append(item['Text'])
    return ' '.join(text)
