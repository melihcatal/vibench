from __future__ import annotations

import boto3

from storage_client import get_bucket_name


def stored_document_ocr(key: str, aws_region: str | None = None) -> dict:
    client = boto3.client("textract", region_name=aws_region)
    response = client.analyze_document(
        Document={"S3Object": {"Bucket": get_bucket_name(), "Name": key}},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response
