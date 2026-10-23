"""OCR on a stored document using Amazon Textract.

Prerequisites:
  * AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set in the environment for boto3.
  * S3 bucket and object key containing the PDF or image.
"""

import os
from storage_models import extract_first_line

# ---- Textract client (uses the same AWS keys as the S3 client) ----
import boto3

client = boto3.client(
    'textract',
    # credentials are taken from the environment because we reuse boto3 config
)

def ocr_document(bucket: str, key: str):
    """Run OCR on a stored document and return structured result.

    Args:
        bucket (str): S3 bucket name.
        key (str): S3 object key.
    Returns:
        dict: Textract response (analysis JSON).
    """
    print(f"Running OCR on s3://{bucket}/{key}")
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {'Bucket': bucket, 'Name': key}
        }
    )
    job_id = response['JobId']
    # Poll for completion (simple implementation)
    import time
    while True:
        status = client.get_document_text_detection(JobId=job_id)
        if status['JobStatus'] in ('SUCCEEDED', 'FAILED'):
            break
        time.sleep(2)
    print(f"OCR job {job_id} finished with status {status['JobStatus']}")
    return status  # full response including Blocks


def get_sample_text(bucket: str, key: str) -> str:
    """Very simple local extractor: first line of the recognized text."""
    result = ocr_document(bucket, key)
    # Textract returns a list of Blocks; we concatenate detected lines.
    lines = [block['Text'] for block in result.get('Blocks', [])
             if block.get('BlockType') == 'LINE']
    return '\\n'.join(lines)

if __name__ == '__main__':
    # Demo usage (requires proper env vars and an S3 object)
    BUCKET = os.getenv('S3_BUCKET') or 'your-bucket'
    KEY = os.getenv('S3_KEY') or 'example.pdf'
    print('First line extracted:', extract_first_line(get_sample_text(BUCKET, KEY)))
