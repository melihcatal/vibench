from __future__ import annotations

import argparse

from storage_client import get_s3_client, get_textract_client, load_settings
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str) -> OCRResult:
    textract = get_textract_client()
    s3 = get_s3_client()
    s3.head_object(Bucket=bucket, Key=key)
    response = textract.detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
    blocks = response.get("Blocks", [])
    text = "\n".join(block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE")
    return OCRResult(bucket=bucket, key=key, text=text, raw_blocks=blocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    args = parser.parse_args()
    settings = load_settings()
    print(run_stored_document_ocr(args.bucket or settings.bucket_name, args.key))
