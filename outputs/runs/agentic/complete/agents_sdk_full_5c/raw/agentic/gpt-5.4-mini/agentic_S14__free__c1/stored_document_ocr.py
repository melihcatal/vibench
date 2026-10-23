from __future__ import annotations

import os

import boto3

from storage_client import create_s3_client, load_storage_config, normalize_boto_error
from storage_models import OCRResult


textract = boto3.client("textract", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def stored_document_ocr(key: str, feature_types: list[str] | None = None) -> dict:
    s3 = create_s3_client()
    bucket = load_storage_config().bucket
    try:
        response = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucket, "Name": key}},
            FeatureTypes=feature_types or ["FORMS", "TABLES"],
        )
        lines = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE" and block.get("Text"):
                lines.append(block["Text"])
        result = OCRResult(object_key=key, text="\n".join(lines), confidence=None, language=None)
        return result.to_dict()
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}
