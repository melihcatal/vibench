from typing import Optional

import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_timestamp


def run_stored_document_ocr(object_key: str, bucket: Optional[str] = None, document_location: str = 'S3Object') -> dict:
    bucket_name = bucket or get_bucket_name()
    client = boto3.client('textract')
    return client.analyze_document(Document={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}, FeatureTypes=['FORMS', 'TABLES'])
