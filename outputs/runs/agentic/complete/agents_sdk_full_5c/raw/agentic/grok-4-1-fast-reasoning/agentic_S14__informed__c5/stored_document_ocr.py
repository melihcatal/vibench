import boto3
from botocore.exceptions import ClientError
from typing import List, Dict

def run_ocr_on_stored_document(bucket: str, key: str) -&gt; str:
    """
    Run OCR on stored document using Amazon Textract detect_document_text with S3 input.
    """
    textract = boto3.client('textract')
    try:
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
        return ' '.join(lines)
    except ClientError as e:
        raise ValueError(f"Amazon Textract OCR failed: {e}")