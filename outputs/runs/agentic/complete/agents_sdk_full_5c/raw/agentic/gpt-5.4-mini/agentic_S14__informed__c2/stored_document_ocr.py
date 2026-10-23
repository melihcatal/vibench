from __future__ import annotations

from typing import Any, Dict

import boto3
from boto3.session import Session

from storage_client import load_storage_config

_TEXTRACT_CLIENT_NAME = "textract"


def run_stored_document_ocr(bucket: str, key: str, language: str = "en") -> Dict[str, Any]:
    load_storage_config(bucket)
    session: Session = boto3.session.Session()
    client = session.client(_TEXTRACT_CLIENT_NAME)
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return {"bucket": bucket, "key": key, "language": language, "text": "\n".join(lines), "raw_blocks": response.get("Blocks", [])}
