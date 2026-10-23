from __future__ import annotations

from storage_client import require_bucket, textract_client
from storage_models import OCRResult, flatten_lines


TEXTRACT_PROVIDER = "Amazon Textract"


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    client = textract_client()
    resolved_bucket = require_bucket(bucket)
    response = client.detect_document_text(Document={"S3Object": {"Bucket": resolved_bucket, "Name": key}})
    blocks = response.get("Blocks", [])
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE"]
    pages = {block.get("Page") for block in blocks if block.get("Page") is not None}
    return OCRResult(bucket=resolved_bucket, key=key, document_text=flatten_lines(lines), page_count=len(pages) or 1)


def run_stored_document_ocr_dict(bucket: str, key: str) -> dict:
    return run_stored_document_ocr(bucket, key).to_dict()
