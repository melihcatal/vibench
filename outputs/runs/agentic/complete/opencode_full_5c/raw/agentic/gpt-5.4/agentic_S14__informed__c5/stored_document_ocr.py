from __future__ import annotations

from storage_client import get_textract_client
from storage_models import OcrDocumentResult


def run_stored_document_ocr(bucket: str, object_name: str) -> OcrDocumentResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": object_name}}
    )
    lines: list[str] = []
    page_numbers: set[int] = set()
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
        page = block.get("Page")
        if isinstance(page, int):
            page_numbers.add(page)
    return OcrDocumentResult(
        bucket=bucket,
        object_name=object_name,
        text="\n".join(lines),
        page_count=max(page_numbers) if page_numbers else None,
        provider="amazon-textract",
        model="DetectDocumentText",
    )
