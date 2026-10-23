from __future__ import annotations

import json
from typing import Optional

from storage_client import get_s3_client, get_textract_client, get_object_content
from storage_models import OcrRequest, OcrResponse, normalize_ocr_response


def run_ocr_on_stored_document(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    textract_client=None,
    s3_client=None,
) -> OcrResponse:
    if s3_client is None:
        s3_client = get_s3_client()
    if textract_client is None:
        textract_client = get_textract_client()

    document_bytes = get_object_content(bucket, key, version_id, client=s3_client)

    response = textract_client.detect_document_text(Document={"Bytes": document_bytes})

    request = OcrRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )

    return normalize_ocr_response(response, request)


def run_ocr_on_stored_document_async(
    bucket: str,
    key: str,
    s3_bucket_name: str,
    s3_prefix: str = "textract-output",
    version_id: Optional[str] = None,
    textract_client=None,
    s3_client=None,
) -> str:
    if s3_client is None:
        s3_client = get_s3_client()
    if textract_client is None:
        textract_client = get_textract_client()

    response = textract_client.start_document_text_detection(
        DocumentLocation={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        OutputConfig={
            "S3Bucket": s3_bucket_name,
            "S3Prefix": s3_prefix,
        },
    )

    return response["JobId"]
