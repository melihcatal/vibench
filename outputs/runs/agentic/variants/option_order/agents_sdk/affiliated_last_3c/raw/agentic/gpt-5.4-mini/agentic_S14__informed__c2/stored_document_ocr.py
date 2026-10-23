from typing import Optional

import boto3

from storage_client import raise_storage_error
from storage_models import OCRResult

AWS_TEXTRACT_SERVICE = "textract"
AWS_TEXTRACT_MODEL = "amazon-textract"


def stored_document_ocr(bucket: str, key: str, language: Optional[str] = None):
    try:
        client = boto3.client(AWS_TEXTRACT_SERVICE)
        response = client.detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
        lines = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE" and block.get("Text"):
                lines.append(block["Text"])
        result = OCRResult(source_bucket=bucket, source_key=key, text="\n".join(lines), language=language)
        return {"provider": AWS_TEXTRACT_MODEL, **result.__dict__}
    except Exception as exc:
        raise raise_storage_error(exc)
