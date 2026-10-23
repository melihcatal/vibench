from __future__ import annotations

from typing import Optional

from storage_client import get_textract_client
from storage_models import OCRResult


def run_stored_document_ocr(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    region_name: Optional[str] = None,
) -> OCRResult:
    textract = get_textract_client(region_name=region_name)
    document_location: dict[str, object] = {
        "S3Object": {"Bucket": bucket, "Name": key}
    }
    if version_id:
        document_location["S3Object"]["Version"] = version_id

    response = textract.detect_document_text(Document=document_location)
    lines: list[str] = []
    page_numbers: set[int] = set()
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
        if "Page" in block:
            page_numbers.add(int(block["Page"]))

    return OCRResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        page_count=max(page_numbers) if page_numbers else 0,
        provider="amazon-textract",
    )
