import boto3
from typing import Dict, Any

def stored_document_ocr(
    bucket: str,
    key: str
) -> str:
    textract_client = boto3.client('textract')
    response: Dict[str, Any] = textract_client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        FeatureTypes=['FORMS', 'TABLES']
    )
    text = ''
    if 'Blocks' in response:
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block.get('Text', '') + '\n'
    return text.strip()