from __future__ import annotations

from typing import Optional

import boto3

from storage_client import get_s3_client, resolve_bucket_name, resolve_key
from storage_models import OcrRequest


AWS_TEXTRACT_CLIENT = boto3.client("textract")


def run_stored_document_ocr(bucket: Optional[str], key: Optional[str], language: Optional[str] = None) -> str:
    request = OcrRequest(bucket=resolve_bucket_name(bucket), key=resolve_key(key), language=language)
    s3 = get_s3_client()
    document = {"S3Object": {"Bucket": request.bucket, "Name": request.key}}
    response = AWS_TEXTRACT_CLIENT.analyze_document(Document=document, FeatureTypes=["TABLES", "FORMS"])
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return "\n".join(lines)
