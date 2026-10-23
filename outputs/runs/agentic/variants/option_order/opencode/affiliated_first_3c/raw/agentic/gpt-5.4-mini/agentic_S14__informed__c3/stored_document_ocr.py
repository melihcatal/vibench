import boto3

from storage_client import get_s3_client
from storage_models import normalize_body


def run_document_ocr(bucket: str, key: str, textract_client=None, s3_client=None) -> dict:
    s3 = s3_client or get_s3_client()
    textract = textract_client or boto3.client("textract")
    obj = s3.get_object(Bucket=bucket, Key=key)
    response = textract.detect_document_text(Document={"Bytes": obj["Body"].read()})
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            lines.append(block["Text"])
    return {"bucket": bucket, "key": key, "text": "
".join(lines), "raw": response}
