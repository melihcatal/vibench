from __future__ import annotations

from storage_client import get_textract_client, merge_document_text
from storage_models import OcrDocumentResult


def run_stored_document_ocr(bucket_name: str, object_name: str) -> OcrDocumentResult:
    textract = get_textract_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_name}}
    )
    pages: dict[int, dict[str, object]] = {}
    for block in response.get("Blocks", []):
        page_number = int(block.get("Page", 1))
        page = pages.setdefault(page_number, {"page_number": page_number, "lines": []})
        if block.get("BlockType") == "LINE":
            page["lines"].append(
                {
                    "text": block.get("Text", ""),
                    "confidence": block.get("Confidence"),
                }
            )
    ordered_pages = [pages[index] for index in sorted(pages)]
    return OcrDocumentResult(
        bucket_name=bucket_name,
        object_name=object_name,
        pages=ordered_pages,
        full_text=merge_document_text(ordered_pages),
        provider="amazon_textract",
    )
