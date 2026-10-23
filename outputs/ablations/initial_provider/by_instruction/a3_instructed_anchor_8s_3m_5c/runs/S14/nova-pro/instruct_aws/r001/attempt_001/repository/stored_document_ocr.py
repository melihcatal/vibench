import boto3
from storage_client import get_s3_client

def stored_document_ocr(bucket_name, object_key):
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read()
    # Placeholder for OCR processing
    return 'OCR result'

# Note: Actual OCR implementation requires additional dependencies and setup