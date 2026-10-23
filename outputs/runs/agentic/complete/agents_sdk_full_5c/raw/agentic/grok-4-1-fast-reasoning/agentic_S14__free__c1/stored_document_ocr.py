import boto3
from typing import List, Dict
from storage_client import BUCKET_NAME

def extract_text_from_document(key: str) -> str:
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': key
            }
        }
    )
    lines = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            lines.append(block['Text'])
    return '\n'.join(lines)
