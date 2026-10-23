from __future__ import annotations

from typing import Any, Dict, List, Optional

from storage_client import get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    region_name: Optional[str] = None,
) -> OCRResult:
    textract = get_textract_client(region_name=region_name)
    document_location: Dict[str, Any] = {"S3Object": {"Bucket": bucket, "Name": key}}
    if version_id:
        document_location["S3Object"]["Version"] = version_id

    response = textract.detect_document_text(Document=document_location)
    blocks: List[Dict[str, Any]] = response.get("Blocks", [])
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE" and block.get("Text")]
    pages = {block.get("Page") for block in blocks if block.get("Page") is not None}
    return OCRResult(
        provider="amazon-textract",
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=len(pages) or None,
        raw_blocks=blocks,
    )
