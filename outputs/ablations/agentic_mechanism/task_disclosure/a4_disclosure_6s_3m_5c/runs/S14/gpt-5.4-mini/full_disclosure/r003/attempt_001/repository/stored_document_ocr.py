import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class StoredDocumentOcrRequest:
    bucket: str
    key: str
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None


def _client(endpoint_url: Optional[str] = None, region_name: Optional[str] = None):
    return boto3.client(
        "textract",
        endpoint_url=endpoint_url or os.getenv("AWS_TEXTRACT_ENDPOINT_URL"),
        region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _document_location(bucket: str, key: str) -> Dict[str, Dict[str, str]]:
    return {"S3Object": {"Bucket": bucket, "Name": key}}


def _extract_text(response: Dict[str, Any]) -> str:
    blocks = response.get("Blocks") or []
    lines = []
    for block in blocks:
        if block.get("BlockType") == "LINE":
            text = block.get("Text")
            if text:
                lines.append(str(text))
    return "\n".join(lines)


def run_stored_document_ocr(bucket: str, key: str, endpoint_url: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = _client(endpoint_url=endpoint_url, region_name=region_name)
    response = client.detect_document_text(Document=_document_location(bucket, key))
    return {
        "bucket": bucket,
        "key": key,
        "text": _extract_text(response),
        "blocks": response.get("Blocks", []),
        "document_metadata": response.get("DocumentMetadata", {}),
        "detect_document_text_model_version": response.get("DetectDocumentTextModelVersion"),
    }


def run_stored_document_ocr_from_request(request: StoredDocumentOcrRequest) -> Dict[str, Any]:
    return run_stored_document_ocr(
        bucket=request.bucket,
        key=request.key,
        endpoint_url=request.endpoint_url,
        region_name=request.region_name,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run Amazon Textract OCR on an S3 document")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--endpoint-url")
    parser.add_argument("--region-name")
    args = parser.parse_args()
    try:
        result = run_stored_document_ocr(args.bucket, args.key, args.endpoint_url, args.region_name)
        print(json.dumps(result, default=str))
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
