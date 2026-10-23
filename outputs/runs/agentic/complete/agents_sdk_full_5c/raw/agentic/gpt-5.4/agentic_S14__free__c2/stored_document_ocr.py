from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from storage_client import get_textract_client
from storage_models import OCRResult


class TextractOCRNotReadyError(RuntimeError):
    pass


def _collect_text_by_page(blocks: List[dict]) -> tuple[str, int]:
    page_lines: Dict[int, List[str]] = defaultdict(list)
    page_count = 0
    for block in blocks:
        if block.get("BlockType") == "PAGE":
            page_count += 1
        if block.get("BlockType") == "LINE":
            page_number = int(block.get("Page", 1))
            text = str(block.get("Text", "")).strip()
            if text:
                page_lines[page_number].append(text)
    ordered_pages = []
    for page_number in sorted(page_lines):
        ordered_pages.append("\n".join(page_lines[page_number]))
    return "\n\n".join(ordered_pages).strip(), page_count or len(page_lines)


def run_stored_document_ocr(bucket: str, key: str, version_id: Optional[str] = None) -> OCRResult:
    textract = get_textract_client()
    document_location = {"S3Object": {"Bucket": bucket, "Name": key}}
    if version_id:
        document_location["S3Object"]["Version"] = version_id

    start = textract.start_document_text_detection(DocumentLocation=document_location)
    job_id = start["JobId"]
    response = textract.get_document_text_detection(JobId=job_id)
    status = response.get("JobStatus")
    if status in {"IN_PROGRESS", "SUCCEEDED"} and response.get("NextToken") is not None:
        blocks = list(response.get("Blocks", []))
        next_token = response.get("NextToken")
        while next_token:
            page = textract.get_document_text_detection(JobId=job_id, NextToken=next_token)
            blocks.extend(page.get("Blocks", []))
            next_token = page.get("NextToken")
        text, pages = _collect_text_by_page(blocks)
        return OCRResult(text=text, pages=pages)
    if status != "SUCCEEDED":
        raise TextractOCRNotReadyError(f"AWS Textract job status: {status}")
    text, pages = _collect_text_by_page(response.get("Blocks", []))
    return OCRResult(text=text, pages=pages)
