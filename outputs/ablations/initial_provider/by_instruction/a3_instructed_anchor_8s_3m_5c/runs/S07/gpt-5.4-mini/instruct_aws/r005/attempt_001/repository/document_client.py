import os
from typing import Any, Dict, List, Optional

import boto3

from document_models import DocumentRequest


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return explicit_region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def make_textract_client(region: Optional[str] = None):
    return boto3.client("textract", region_name=get_aws_region(region))


def load_document_request(payload: Dict[str, Any]) -> DocumentRequest:
    return DocumentRequest(
        bucket=payload["bucket"],
        key=payload["key"],
        mime_type=payload.get("mime_type"),
        feature_types=list(payload.get("feature_types", [])),
        aws_region=payload.get("aws_region"),
    )


def s3_document_reference(request: DocumentRequest) -> Dict[str, str]:
    return {"S3Object": {"Bucket": request.bucket, "Name": request.key}}


def collect_block_texts(blocks: List[Dict[str, Any]], block_type: Optional[str] = None) -> List[str]:
    texts = []
    for block in blocks:
        if block_type and block.get("BlockType") != block_type:
            continue
        text = block.get("Text") or ""
        if text:
            texts.append(text)
    return texts
