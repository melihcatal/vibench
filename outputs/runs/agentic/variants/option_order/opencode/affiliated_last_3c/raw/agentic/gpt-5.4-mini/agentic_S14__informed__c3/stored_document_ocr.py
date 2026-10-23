from typing import Optional

import boto3

from storage_client import get_bucket_name


def run_document_ocr(
    bucket: Optional[str], key: str, region_name: Optional[str] = None
):
    client = boto3.client("textract", region_name=region_name)
    bucket_name = get_bucket_name(bucket)
    return client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": key}}
    )
