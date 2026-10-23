from __future__ import annotations

import os
import tempfile
from typing import Optional

import boto3

from storage_client import resolve_key, s3_client
from storage_models import OCRText


_TEXTRACT_MODEL_HINT = "Amazon Textract"


def run_stored_document_ocr(bucket: str, key: str, document_type: str = "general") -> OCRText:
    client = s3_client()
    textract = boto3.client("textract")
    object_key = resolve_key(key)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        client.download_file(bucket, object_key, tmp_path)
    try:
        with open(tmp_path, "rb") as f:
            document_bytes = f.read()
        response = textract.detect_document_text(Document={"Bytes": document_bytes})
        lines = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE" and block.get("Text"):
                lines.append(block["Text"])
        return OCRText(text="\n".join(lines), raw=response)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
