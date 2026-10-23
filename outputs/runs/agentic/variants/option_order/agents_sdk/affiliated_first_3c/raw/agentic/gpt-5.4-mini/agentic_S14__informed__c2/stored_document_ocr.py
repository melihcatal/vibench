from __future__ import annotations

from typing import Optional

import boto3

from storage_client import resolve_bucket
from storage_models import OCRRequest


textract = boto3.client("textract")


def stored_document_ocr(bucket: Optional[str], key: str, language: Optional[str] = None) -> dict:
    request = OCRRequest(bucket=resolve_bucket(bucket), key=key, language=language)
    document = {"S3Object": {"Bucket": request.bucket, "Name": request.key}}
    kwargs = {"Document": document}
    if request.language:
        kwargs["FeatureTypes"] = ["TABLES", "FORMS"]
    response = textract.detect_document_text(**kwargs)
    blocks = response.get("Blocks", [])
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE"]
    return {"bucket": request.bucket, "key": request.key, "text": "\n".join(lines), "blocks": blocks}
