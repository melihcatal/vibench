import boto3
from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ObjectMetadataRequest


def stored_document_ocr(request: ObjectMetadataRequest) -> str:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    obj = s3.get_object(Bucket=bucket, Key=request.key)
    return obj['Body'].read().decode('utf-8', errors='ignore')
