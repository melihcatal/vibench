import os
from typing import Any, Dict

import boto3

from document_client import get_textract_client
from document_models import OCRRequest, OCRResponse, normalize_text


def extract_text(document: Any = None, *, bucket: str = None, key: str = None, bytes_data: bytes = None) -> OCRResponse:
    client = get_textract_client()
    if bytes_data is not None:
        response = client.detect_document_text(Document={"Bytes": bytes_data})
    else:
        if not bucket or not key:
            raise ValueError("bucket and key are required when bytes_data is not provided")
        response = client.detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
    return OCRResponse(raw=response, text=normalize_text(response))
