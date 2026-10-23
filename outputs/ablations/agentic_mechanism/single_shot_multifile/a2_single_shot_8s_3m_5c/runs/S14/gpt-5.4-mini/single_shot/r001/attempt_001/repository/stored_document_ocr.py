from io import BytesIO
from typing import Optional

import boto3

from storage_client import get_s3_client, get_storage_config
from storage_models import ObjectMetadataRequest, coerce_body_bytes


textract = boto3.client("textract")


def run_stored_document_ocr(bucket: str, key: str) -> dict:
    config = get_storage_config()
    s3 = get_s3_client(config)
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj["Body"].read()
    response = textract.detect_document_text(Document={"Bytes": data})
    return response
