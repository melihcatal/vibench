from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    blocks = response.get("Blocks", [])
    lines = [
        block.get("Text", "")
        for block in blocks
        if block.get("BlockType") == "LINE" and block.get("Text")
    ]
    page_numbers = {
        block.get("Page") for block in blocks if block.get("Page") is not None
    }
    return OCRResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=len(page_numbers) or 1,
        raw_blocks=blocks,
    )
