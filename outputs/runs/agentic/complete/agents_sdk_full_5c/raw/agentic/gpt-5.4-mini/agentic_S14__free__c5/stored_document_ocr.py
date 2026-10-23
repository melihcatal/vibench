from __future__ import annotations

import argparse
from typing import Optional

import boto3

from storage_client import load_storage_config
from storage_models import TextExtractionResult

TEXTRACT_CLIENT = "textract"


def run_stored_document_ocr(key: str, bucket: Optional[str] = None) -> TextExtractionResult:
    cfg = load_storage_config(bucket)
    s3 = boto3.client("s3", region_name=cfg.region, endpoint_url=cfg.endpoint_url)
    textract = boto3.client(TEXTRACT_CLIENT, region_name=cfg.region)
    obj = s3.get_object(Bucket=cfg.bucket, Key=key)
    payload = obj["Body"].read()
    resp = textract.detect_document_text(Document={"Bytes": payload})
    lines = [item["Text"] for item in resp.get("Blocks", []) if item.get("BlockType") == "LINE" and item.get("Text")]
    return TextExtractionResult(bucket=cfg.bucket, key=key, text="\n".join(lines), language="en", provider="aws-textract")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OCR on a stored S3 document using AWS Textract")
    parser.add_argument("key")
    parser.add_argument("--bucket")
    args = parser.parse_args()
    print(run_stored_document_ocr(args.key, bucket=args.bucket))


if __name__ == "__main__":
    main()
