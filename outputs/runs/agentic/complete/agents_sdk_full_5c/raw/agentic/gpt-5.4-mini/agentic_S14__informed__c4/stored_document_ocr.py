from __future__ import annotations

import io

from boto3.session import Session

from storage_client import coerce_bucket, get_s3_client
from storage_models import OCRResult


def stored_document_ocr(bucket: str, key: str, region_name: str | None = None) -> OCRResult:
    s3 = get_s3_client()
    bucket = coerce_bucket(bucket)
    obj = s3.get_object(Bucket=bucket, Key=key)
    document_bytes = obj["Body"].read()
    textract = Session(region_name=region_name).client("textract")
    response = textract.detect_document_text(Document={"Bytes": document_bytes})
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return OCRResult(bucket=bucket, key=key, text="\n".join(lines), pages=lines)
