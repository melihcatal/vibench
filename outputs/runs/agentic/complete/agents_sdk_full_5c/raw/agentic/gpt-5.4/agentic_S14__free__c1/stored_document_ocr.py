from __future__ import annotations

from typing import Optional

from storage_client import get_default_bucket, get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str, region: Optional[str] = None) -> OCRResult:
    resolved_bucket = get_default_bucket(bucket)
    textract = get_textract_client(region=region)
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": resolved_bucket,
                "Name": key,
            }
        }
    )

    blocks = response.get("Blocks", [])
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE"]
    page_numbers = {block.get("Page") for block in blocks if block.get("Page") is not None}

    return OCRResult(
        provider="aws_textract",
        bucket=resolved_bucket,
        key=key,
        pages=len(page_numbers) if page_numbers else 1,
        text="\n".join(line for line in lines if line),
        blocks=blocks,
    )
