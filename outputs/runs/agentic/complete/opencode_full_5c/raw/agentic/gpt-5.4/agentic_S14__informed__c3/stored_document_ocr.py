from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines = []
    page_numbers: set[int] = set()
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
        if "Page" in block:
            page_numbers.add(int(block["Page"]))
    return OCRResult(
        bucket=bucket,
        key=key,
        job_id=response.get("DetectDocumentTextModelVersion"),
        text="\n".join(lines),
        page_count=len(page_numbers) or 1,
    )
