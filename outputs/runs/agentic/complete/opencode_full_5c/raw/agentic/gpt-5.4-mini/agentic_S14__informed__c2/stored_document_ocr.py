import boto3

from storage_client import get_s3_client


def run_stored_document_ocr(bucket: str, key: str, output_bucket: str = None, output_prefix: str = 'ocr/'):
    client = boto3.client('textract')
    result = client.detect_document_text(Document={'S3Object': {'Bucket': bucket, 'Name': key}})
    return result
