import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3


@dataclass(frozen=True)
class StoredDocumentOCRResult:
    bucket: str
    key: str
    text: str
    pages: List[Dict[str, Any]]
    job_status: Optional[str] = None
    model_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
    }
    if region:
        kwargs["region_name"] = region
    return boto3.client("textract", **kwargs)


def run_stored_document_ocr(
    bucket: str,
    key: str,
    language: Optional[str] = None,
    page_numbers: Optional[List[int]] = None,
) -> StoredDocumentOCRResult:
    params: Dict[str, Any] = {"Document": {"S3Object": {"Bucket": bucket, "Name": key}}}
    if language:
        params["FeatureTypes"] = ["FORMS", "TABLES"]
    response = _client().analyze_document(**params)
    blocks = response.get("Blocks", [])
    lines: List[str] = []
    pages: List[Dict[str, Any]] = []
    for block in blocks:
        if block.get("BlockType") == "LINE":
            if page_numbers and block.get("Page") not in page_numbers:
                continue
            text = block.get("Text")
            if text:
                lines.append(text)
        if block.get("BlockType") == "PAGE":
            pages.append({"page": block.get("Page"), "confidence": block.get("Confidence")})
    return StoredDocumentOCRResult(
        bucket=bucket,
        key=key,
        text="\n".join(lines),
        pages=pages,
        job_status=response.get("JobStatus"),
        model_id="amazon-textract",
        raw=response,
    )


__all__ = ["StoredDocumentOCRResult", "run_stored_document_ocr"]
