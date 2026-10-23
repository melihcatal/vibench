from __future__ import annotations

from typing import Optional

from storage_client import get_bucket_name, get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(key: str, bucket: Optional[str] = None, region_name: Optional[str] = None) -> OCRResult:
    textract = get_textract_client(region_name=region_name)
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": get_bucket_name(bucket),
                "Name": key,
            }
        }
    )

    lines = []
    page_count = 0
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "PAGE":
            page_count += 1
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])

    return OCRResult(
        bucket=get_bucket_name(bucket),
        key=key,
        text="\n".join(lines),
        page_count=page_count,
    )
