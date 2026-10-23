import os

import boto3

from storage_client import bucket_name, client


def stored_document_ocr(bucket: str | None, key: str):
    s3 = client()
    textract = boto3.client(
        "textract",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    obj = s3.get_object(Bucket=bucket_name(bucket), Key=key)
    return textract.detect_document_text(Document={"Bytes": obj["Body"].read()})
