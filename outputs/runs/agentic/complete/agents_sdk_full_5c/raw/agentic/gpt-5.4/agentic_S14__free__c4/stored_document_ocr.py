from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OCRResult


def extract_document_text_from_s3(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        }
    )

    lines: list[str] = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])

    page_numbers = {
        block.get("Page")
        for block in response.get("Blocks", [])
        if block.get("BlockType") == "PAGE"
    }

    return OCRResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=len([p for p in page_numbers if p is not None]) or 1,
        provider_job_id=response.get("DetectDocumentTextModelVersion"),
    )
