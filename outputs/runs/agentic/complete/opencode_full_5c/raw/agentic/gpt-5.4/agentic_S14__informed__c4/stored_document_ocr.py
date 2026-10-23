from __future__ import annotations

from storage_client import get_s3_client, get_textract_client
from storage_models import StoredDocumentOcrResult


def run_stored_document_ocr(bucket: str, key: str) -> StoredDocumentOcrResult:
    s3 = get_s3_client()
    textract = get_textract_client()
    s3.head_object(Bucket=bucket, Key=key)
    response = textract.detect_document_text(
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
        if block.get("BlockType") == "LINE" and block.get("Page") is not None
    }
    return StoredDocumentOcrResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=len(pages) or 1,
        provider="amazon-textract",
        model="DetectDocumentText",
    )
