import boto3
from botocore.exceptions import ClientError
from typing import Dict

from storage_client import get_aws_credentials

def run_ocr_on_stored_document(
    bucket: str,
    document_key: str
) -> str:
    creds = get_aws_credentials()
    textract_client = boto3.client('textract', **creds)
    
    try:
        response = textract_client.detect_document_text(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': document_key
                }
            }
        )
        
        full_text = ''
        if 'Blocks' in response:
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE' and 'Text' in block:
                    full_text += block['Text'] + '\\n'
        
        return full_text.strip()
    except ClientError as e:
        raise RuntimeError(f"Textract OCR failed: {e}") from e
