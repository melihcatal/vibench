import json
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import StoredDocumentOcrResult

REKOGNITION_MODEL = "aws-rekognition-text-detection"


def run_stored_document_ocr(bucket: str, key: str) -> StoredDocumentOcrResult:
    s3 = get_s3_client()
    rekognition = boto3.client("rekognition")
    bucket_name = resolve_bucket_name(bucket)
    object_key = resolve_object_key(key)
    try:
        response = rekognition.detect_text(Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}})
        lines = []
        best_lang = None
        best_conf = None
        for item in response.get("TextDetections", []):
            if item.get("Type") == "LINE" and item.get("DetectedText"):
                lines.append(item["DetectedText"])
                if best_conf is None or float(item.get("Confidence", 0.0)) > float(best_conf):
                    best_conf = float(item.get("Confidence", 0.0))
                    best_lang = item.get("DetectedLanguage")
        return StoredDocumentOcrResult(bucket=bucket_name, key=object_key, text="\n".join(lines), language_code=best_lang, confidence=best_conf)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"OCR failed for s3://{bucket_name}/{object_key} using {REKOGNITION_MODEL}: {exc}") from exc


__all__ = ["run_stored_document_ocr"]
