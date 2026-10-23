from __future__ import annotations

from storage_client import create_textract_client
from storage_models import OCRResult, StorageObjectRef



def run_stored_document_ocr(bucket: str, key: str, version_id: str | None = None) -> OCRResult:
    client = create_textract_client()
    document_location = {"S3Object": {"Bucket": bucket, "Name": key}}
    if version_id:
        document_location["S3Object"]["Version"] = version_id
    response = client.detect_document_text(Document=document_location)
    lines = []
    blocks = response.get("Blocks", [])
    for block in blocks:
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    page_count = sum(1 for block in blocks if block.get("BlockType") == "PAGE") or 1
    return OCRResult(
        object_ref=StorageObjectRef(bucket=bucket, key=key, version_id=version_id),
        text="\n".join(lines),
        page_count=page_count,
        provider_job_id=response.get("DetectDocumentTextModelVersion"),
        blocks=blocks,
    )
