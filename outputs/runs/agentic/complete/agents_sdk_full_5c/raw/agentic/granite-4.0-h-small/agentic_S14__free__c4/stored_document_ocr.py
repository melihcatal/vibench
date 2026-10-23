import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def ocr_stored_document(bucket_name: str, object_key: str) -> str:
    """Run OCR on a stored document (e.g., PDF, image) using AWS Textract.

    Returns extracted plain text.
    """
    client = get_s3_client()
    # Initiate Textract job asynchronously
    response = boto3.client('textract').start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    )
    job_id = response['JobId']
    # Poll job status
    while True:
        status = boto3.client('textract').get_document_text_detection(JobId=job_id)['JobStatus']
        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED':
            raise RuntimeError('OCR job failed')
        # Short poll interval
        time.sleep(2)
    # Retrieve results
    result = boto3.client('textract').get_document_text_detection(JobId=job_id)
    text_blocks = result.get('Blocks', [])
    text = ''.join(block['Text'] for block in text_blocks if block['BlockType'] == 'LINE')
    return text