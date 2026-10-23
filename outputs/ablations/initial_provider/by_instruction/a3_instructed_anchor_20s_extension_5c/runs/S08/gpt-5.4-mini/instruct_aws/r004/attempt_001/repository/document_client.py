import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

from document_models import DocumentRequest, DocumentResponse, FieldValue, normalize_field_name


def load_document_config() -> Dict[str, Any]:
    return {
        "aws_region": os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        "textract_endpoint_url": os.environ.get("AWS_TEXTRACT_ENDPOINT_URL"),
        "s3_bucket": os.environ.get("DOCUMENT_S3_BUCKET"),
    }


def create_textract_client(region: Optional[str] = None) -> BaseClient:
    cfg = load_document_config()
    session = boto3.Session(region_name=region or cfg["aws_region"])
    kwargs: Dict[str, Any] = {}
    if cfg["textract_endpoint_url"]:
        kwargs["endpoint_url"] = cfg["textract_endpoint_url"]
    return session.client("textract", **kwargs)


def build_textract_query(field_name: str, alias: Optional[str] = None) -> Dict[str, str]:
    return {
        "Text": f"Extract {field_name}",
        "Alias": alias or normalize_field_name(field_name),
    }


def response_to_document_response(raw: Dict[str, Any]) -> DocumentResponse:
    fields: Dict[str, FieldValue] = {}
    for key, value in raw.get("fields", {}).items():
        fields[normalize_field_name(key)] = FieldValue(
            value=value.get("value"),
            confidence=value.get("confidence"),
            source=value.get("source", "aws_textract"),
        )
    return DocumentResponse(fields=fields, raw=raw)


def request_to_payload(request: DocumentRequest) -> Dict[str, Any]:
    payload = asdict(request)
    if request.document_bytes is not None:
        payload["document_bytes"] = request.document_bytes
    return payload
