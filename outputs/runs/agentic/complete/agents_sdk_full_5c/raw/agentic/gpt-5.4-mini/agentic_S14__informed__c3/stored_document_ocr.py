from __future__ import annotations

import io
from typing import Any

import boto3
from botocore.config import Config

from storage_client import create_storage_client
from storage_models import OCRRequest, NormalizedTextResult, coerce_text


def run_stored_document_ocr(request: OCRRequest) -> NormalizedTextResult:
    # Amazon Textract reads directly from S3 objects.
    textract = boto3.client("textract", config=Config())
    s3 = create_storage_client("s3")
    obj = s3.get_object(Bucket=request.bucket, Key=request.key)
    payload = obj["Body"].read()
    response = textract.detect_document_text(Document={"Bytes": payload})
    lines: list[str] = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(coerce_text(block.get("Text")))
    return NormalizedTextResult(text="\n".join(lines).strip(), raw=response)
