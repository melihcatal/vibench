from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OCRDocumentResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRDocumentResult:
    client = get_textract_client()
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines = [
        block["Text"]
        for block in response.get("Blocks", [])
        if block.get("BlockType") == "LINE" and block.get("Text")
    ]
    pages = {
        block.get("Page")
        for block in response.get("Blocks", [])
        if block.get("Page") is not None
    }
    return OCRDocumentResult(
        bucket=bucket,
        key=key,
        provider="amazon-textract",
        text="\n".join(lines),
        page_count=len(pages) if pages else 1,
        lines=lines,
    )
