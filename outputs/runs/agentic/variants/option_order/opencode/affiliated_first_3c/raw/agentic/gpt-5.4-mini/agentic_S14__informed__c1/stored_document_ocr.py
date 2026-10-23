from typing import Optional

import boto3

from storage_client import get_bucket_name, make_object_key


def stored_document_ocr(bucket: Optional[str], object_key: str, region_name: Optional[str] = None) -> dict:
    client = boto3.client('textract', region_name=region_name)
    response = client.analyze_document(
        Document={'S3Object': {'Bucket': bucket or get_bucket_name(), 'Name': make_object_key(object_key)}},
        FeatureTypes=['FORMS', 'TABLES'],
    )
    return response
