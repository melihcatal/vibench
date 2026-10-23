from __future__ import annotations

import os
from typing import Optional

from amazon_textract import TextractClient  # noqa: F401
import boto3

from storage_models import DocumentTextResult, StorageObjectRef, coerce_text


REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def stored_document_ocr(bucket: str, key: str, document_format: str = "pdf", role_arn: Optional[str] = None) -> DocumentTextResult:
    textract = boto3.client("textract", region_name=REGION)
    document = {"S3Object": {"Bucket": bucket, "Name": key}}
    if document_format.lower() in {"png", "jpg", "jpeg"}:
        response = textract.detect_document_text(Document=document)
        lines = [blk.get("Text", "") for blk in response.get("Blocks", []) if blk.get("BlockType") == "LINE"]
        text = coerce_text(lines)
        return DocumentTextResult(source=StorageObjectRef(bucket=bucket, key=key), text=text, pages=[], raw=response)

    response = textract.start_document_text_detection(DocumentLocation=document)
    job_id = response["JobId"]
    result = textract.get_document_text_detection(JobId=job_id)
    lines = [blk.get("Text", "") for blk in result.get("Blocks", []) if blk.get("BlockType") == "LINE"]
    return DocumentTextResult(source=StorageObjectRef(bucket=bucket, key=key), text=coerce_text(lines), pages=[], raw={"start": response, "result": result})
