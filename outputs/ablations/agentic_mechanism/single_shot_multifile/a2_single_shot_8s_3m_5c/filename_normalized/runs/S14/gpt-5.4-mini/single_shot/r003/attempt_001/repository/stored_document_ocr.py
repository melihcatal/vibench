from typing import Any, Dict

import boto3

from storage_client import create_s3_client, get_storage_config
from storage_models import read_bytes_source


def stored_document_ocr(bucket: str, key: str, textract_document_format: str = "PDF") -> Dict[str, Any]:
    config = get_storage_config()
    s3_client = create_s3_client(config)
    textract = boto3.client("textract", region_name=config.aws_region)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()
    response = textract.detect_document_text(
        Document={"Bytes": body}
    )
    blocks = response.get("Blocks", [])
    lines = [b["Text"] for b in blocks if b.get("BlockType") == "LINE" and b.get("Text")]
    return {"bucket": bucket, "key": key, "lines": lines, "text": "\n".join(lines)}
