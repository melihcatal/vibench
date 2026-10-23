import json
import os
from typing import Any, Dict

import boto3

from document_models import DocumentExtractionRequest, DocumentExtractionResponse


def get_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "textract_role_arn": os.getenv("AWS_TEXTRACT_ROLE_ARN"),
    }


def textract_client():
    return boto3.client("textract", region_name=get_config()["aws_region"])


def parse_textract_response(payload: Dict[str, Any]) -> DocumentExtractionResponse:
    fields = {}
    confidence = {}
    blocks = payload.get("Blocks", [])
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET" and block.get("EntityTypes") == ["KEY"]:
            text = block.get("Text", "")
            if text:
                fields[text.lower().replace(" ", "_")] = text
                confidence[text.lower().replace(" ", "_")] = float(block.get("Confidence", 0.0))
    return DocumentExtractionResponse(provider="aws-textract", fields=fields, confidence=confidence, raw=payload)


def build_document_request(document_uri: str = None, document_bytes: bytes = None, mime_type: str = "application/pdf") -> DocumentExtractionRequest:
    return DocumentExtractionRequest(document_uri=document_uri, document_bytes=document_bytes, mime_type=mime_type)


def to_json_payload(response: DocumentExtractionResponse) -> str:
    return json.dumps({"provider": response.provider, "fields": response.fields, "confidence": response.confidence, "raw": response.raw})
