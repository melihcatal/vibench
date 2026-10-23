import os

import boto3

from storage_client import get_s3_client


def stored_document_ocr(bucket: str, key: str):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket, Key=key)
    textract = boto3.client(
        "textract", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    return textract.detect_document_text(Document={"Bytes": obj["Body"].read()})
