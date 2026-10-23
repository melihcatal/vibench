import boto3
import os
from typing import Optional

def stored_document_ocr(
    bucket: str,
    key: str,
    region: Optional[str] = 'us-east-1'
) -> str:
    client = boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text.strip()
