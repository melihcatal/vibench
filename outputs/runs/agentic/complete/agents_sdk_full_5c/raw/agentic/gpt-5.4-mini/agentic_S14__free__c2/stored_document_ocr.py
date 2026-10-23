from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, get_textract_client, load_storage_config
from storage_models import OcrResult, normalize_text_chunks


def stored_document_ocr(bucket: Optional[str], key: str, document_type: str = "PDF") -> OcrResult:
    resolved_bucket = bucket or load_storage_config().bucket
    if not resolved_bucket:
        raise ValueError("bucket is required")

    textract = get_textract_client()
    s3 = get_s3_client()
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": resolved_bucket, "Name": key}},
    )
    blocks = response.get("Blocks", [])
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE"]
    text = normalize_text_chunks(lines)
    confidence = None
    if blocks:
        confidences = [block.get("Confidence") for block in blocks if block.get("Confidence") is not None]
        if confidences:
            confidence = sum(confidences) / len(confidences)
    s3.head_object(Bucket=resolved_bucket, Key=key)
    return OcrResult(text=text, language_code=document_type, confidence=confidence)
