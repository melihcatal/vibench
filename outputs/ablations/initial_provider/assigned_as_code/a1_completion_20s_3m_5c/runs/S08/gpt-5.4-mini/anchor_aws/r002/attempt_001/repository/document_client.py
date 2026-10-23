import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class DocumentClientConfig:
    region: Optional[str] = None
    confidence_threshold: float = 0.0


def load_config(config: Optional[Dict[str, Any]] = None) -> DocumentClientConfig:
    config = config or {}
    return DocumentClientConfig(
        region=config.get("region") or os.getenv("AWS_REGION"),
        confidence_threshold=float(config.get("confidence_threshold", 0.0)),
    )


def get_textract_client(config: Optional[Dict[str, Any]] = None):
    settings = load_config(config)
    return boto3.client("textract", region_name=settings.region)


def document_bytes(payload: Dict[str, Any]) -> bytes:
    return payload["document_bytes"]
