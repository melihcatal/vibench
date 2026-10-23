'''OCR a stored Azure Blob document using AWS Textract.'''
import io
import boto3
from PIL import Image
from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import ObjectMetadataResult
from typing import Tuple, List

def stored_document_ocr(container_name: str, blob_name: str) -> Tuple[str, List[str]]:
    """Perform OCR on a PDF/JPEG stored in Azure Blob Storage, then extract text.

    Args:
        container_name: Azure storage container.
        blob_name: Blob file name (document).

    Returns:
        A tuple (content_type, list_of_text_blocks).
    """
    # Retrieve blob content as bytes
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_bytes = blob_client.download_blob().readall()

    # Upload to an S3 bucket for Textract (placeholder bucket - ensure bucket exists)
    s3 = boto3.client('s3')
    s3_bucket = os.getenv('TEXTRACT_S3_BUCKET')
    if not s3_bucket:
        raise RuntimeError('TEXTRACT_S3_BUCKET env var not set')
    s3_key = f'temp/{blob_name}'
    s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=blob_bytes)

    # Call Textract
    textract = boto3.client('textract')
    response = textract.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}})
    job_id = response['JobId']
    # Poll for completion
    while True:
        status = textract.get_document_text_detection(JobId=job_id)['JobStatus']
        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED':
            raise RuntimeError('OCR job failed')
        # Wait 2 seconds
        import time; time.sleep(2)

    # Get results
    result = textract.get_document_text_detection(JobId=job_id)
    lines = [block['Text'] for block in result['Blocks'] if block['BlockType'] == 'LINE']
    # Clean up temporary S3 object (optional)
    s3.delete_object(Bucket=s3_bucket, Key=s3_key)
    # Infer content type from blob metadata
    metadata: ObjectMetadataResult = blob_client.get_blob_properties()
    return metadata['content_type'], lines
