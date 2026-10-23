import base64
from typing import Any

import boto3

from storage_client import storage_client
from storage_models import OcrResponse


def stored_document_ocr(
    bucket: str, object_name: str, region_name: str = None
) -> OcrResponse:
    s3 = storage_client("s3", region_name=region_name)
    textract = boto3.client("textract", region_name=region_name or s3.meta.region_name)
    obj = s3.get_object(Bucket=bucket, Key=object_name)
    data = obj["Body"].read()
    result = textract.detect_document_text(Document={"Bytes": data})
    lines = []
    for block in result.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return OcrResponse(
        bucket=bucket, object_name=object_name, text="\n".join(lines), raw=result
    )
