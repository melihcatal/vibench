from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines: list[str] = []
    page_count = 0
    for block in response.get("Blocks", []):
        block_type = block.get("BlockType")
        if block_type == "PAGE":
            page_count += 1
        elif block_type == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return OCRResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=page_count,
        provider_job_id=response.get("DetectDocumentTextModelVersion"),
    )
