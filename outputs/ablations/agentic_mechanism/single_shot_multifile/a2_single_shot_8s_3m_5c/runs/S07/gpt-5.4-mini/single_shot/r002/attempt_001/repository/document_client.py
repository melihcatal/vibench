import base64
import os
from functools import lru_cache
from typing import Optional

import boto3

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
AWS_SESSION_TOKEN_ENV = "AWS_SESSION_TOKEN"
TEXTRACT_ENDPOINT_ENV = "TEXTRACT_ENDPOINT_URL"


@lru_cache(maxsize=1)
def get_aws_session():
    session_kwargs = {}
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV)
    if region:
        session_kwargs["region_name"] = region
    access_key = os.getenv(AWS_ACCESS_KEY_ID_ENV)
    secret_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV)
    token = os.getenv(AWS_SESSION_TOKEN_ENV)
    if access_key and secret_key:
        session_kwargs["aws_access_key_id"] = access_key
        session_kwargs["aws_secret_access_key"] = secret_key
    if token:
        session_kwargs["aws_session_token"] = token
    return boto3.session.Session(**session_kwargs)


def get_ocr_endpoint(action: str) -> str:
    endpoint = os.getenv(TEXTRACT_ENDPOINT_ENV)
    if endpoint:
        return endpoint
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV) or "us-east-1"
    return f"https://textract.{region}.amazonaws.com"


def load_document_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def build_document_request_headers(content: bytes, mime_type: Optional[str] = None) -> dict:
    headers = {
        "Content-Type": mime_type or "application/octet-stream",
        "X-Amz-Target": "Textract.DetectDocumentText",
        "Accept": "application/json",
    }
    return headers
