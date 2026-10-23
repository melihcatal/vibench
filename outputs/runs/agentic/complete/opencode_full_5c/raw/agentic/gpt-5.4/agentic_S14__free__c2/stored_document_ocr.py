from __future__ import annotations

from storage_client import get_textract_client, require_bucket
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    bucket_name = require_bucket(bucket)
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": key}}
    )
    lines = [
        block.get("Text", "")
        for block in response.get("Blocks", [])
        if block.get("BlockType") == "LINE" and block.get("Text")
    ]
    pages = {
        block.get("Page")
        for block in response.get("Blocks", [])
        if block.get("Page") is not None
    }
    metadata = response.get("DocumentMetadata", {})
    job_id = response.get("ResponseMetadata", {}).get("RequestId", "")
    return OCRResult(
        source_bucket=bucket_name,
        source_key=key,
        job_status="SUCCEEDED",
        text="\n".join(lines),
        page_count=metadata.get("Pages") or len(pages),
        provider_job_id=job_id,
    )
