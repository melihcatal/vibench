from __future__ import annotations

from typing import Optional

from storage_client import get_textract_client
from storage_models import OCRResult, join_text_parts


def run_stored_document_ocr(bucket: str, key: str, region_name: Optional[str] = None) -> OCRResult:
    textract = get_textract_client(region_name=region_name)
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines = [
        block.get("Text", "")
        for block in response.get("Blocks", [])
        if block.get("BlockType") == "LINE"
    ]
    pages = {block.get("Page") for block in response.get("Blocks", []) if block.get("Page") is not None}
    return OCRResult(
        provider="Amazon Textract",
        object_bucket=bucket,
        object_key=key,
        text=join_text_parts(lines),
        page_count=len(pages) or None,
        raw=response,
    )
