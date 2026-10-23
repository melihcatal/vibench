import base64
import os
from pathlib import Path
from typing import Any, Optional

import boto3


def build_textract_client(region_name: Optional[str] = None):
    return boto3.client("textract", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def coerce_document_bytes(document: Any) -> bytes:
    if isinstance(document, bytes):
        return document
    if isinstance(document, str):
        if document.startswith("data:") and "," in document:
            return base64.b64decode(document.split(",", 1)[1])
        path = Path(document)
        if path.exists():
            return path.read_bytes()
        return document.encode("utf-8")
    if hasattr(document, "read"):
        return document.read()
    if isinstance(document, dict) and "bytes" in document:
        value = document["bytes"]
        return value if isinstance(value, bytes) else bytes(value)
    raise TypeError("Unsupported document input")


def infer_document_source(document: Any, provider: str) -> str:
    if isinstance(document, dict) and document.get("source"):
        return str(document["source"])
    return provider
