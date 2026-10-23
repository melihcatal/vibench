from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

from document_models import DocumentInput

AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def textract_client(region_name: str = AWS_REGION) -> BaseClient:
    session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region_name,
    )
    return session.client("textract")


def load_document_input(content: Optional[bytes] = None, path: Optional[str] = None, mime_type: str = "application/pdf") -> DocumentInput:
    if content is None and path:
        with open(path, "rb") as fh:
            content = fh.read()
    return DocumentInput(content=content, path=path, mime_type=mime_type)


def textract_bytes_payload(document: DocumentInput) -> Dict[str, Any]:
    if document.content is None:
        raise ValueError("document.content is required for byte-based Textract operations")
    return {"Bytes": document.content}


def textract_s3_payload(bucket: str, key: str) -> Dict[str, Any]:
    return {"S3Object": {"Bucket": bucket, "Name": key}}


def as_payload_dict(document: DocumentInput) -> Dict[str, Any]:
    return {k: v for k, v in asdict(document).items() if v is not None}
