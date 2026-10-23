from __future__ import annotations

from typing import Optional

from storage_client import get_textract_client, require_bucket
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str, version_id: Optional[str] = None, region_name: Optional[str] = None) -> OCRResult:
    textract = get_textract_client(region_name)
    document_location = {"S3Object": {"Bucket": require_bucket(bucket), "Name": key}}
    if version_id:
        document_location["S3Object"]["Version"] = version_id

    response = textract.detect_document_text(Document=document_location)
    lines = [block.get("Text", "") for block in response.get("Blocks", []) if block.get("BlockType") == "LINE"]
    pages = {block.get("Page") for block in response.get("Blocks", []) if block.get("Page") is not None}
    return OCRResult(
        bucket=document_location["S3Object"]["Bucket"],
        key=key,
        text="\n".join(line for line in lines if line),
        page_count=max(len(pages), 1 if lines else 0),
        provider_job_id=response.get("DetectDocumentTextModelVersion"),
    )
