import boto3
from typing import List, Dict

def stored_document_ocr(bucket: str, object_key: str) -> str:
    """
    Run OCR on a stored document object using Amazon Textract.
    """
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': object_key
            }
        }
    )
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text.strip()