import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class SecurityConfig:
    region_name: str
    key_id: str
    signing_key_id: str
    kms_endpoint_url: Optional[str] = None


def load_config() -> SecurityConfig:
    return SecurityConfig(
        region_name=os.environ.get(
            "AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        ),
        key_id=os.environ["KMS_KEY_ID"],
        signing_key_id=os.environ.get("KMS_SIGNING_KEY_ID", os.environ["KMS_KEY_ID"]),
        kms_endpoint_url=os.environ.get("KMS_ENDPOINT_URL"),
    )


def kms_client(config: Optional[SecurityConfig] = None):
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {"region_name": cfg.region_name}
    if cfg.kms_endpoint_url:
        kwargs["endpoint_url"] = cfg.kms_endpoint_url
    return boto3.client("kms", **kwargs)


def encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    for key in ("CiphertextBlob", "Plaintext", "Signature"):
        if key in normalized and isinstance(normalized[key], (bytes, bytearray)):
            normalized[key] = encode_bytes(bytes(normalized[key]))
    return normalized


def json_response(data: Dict[str, Any]) -> str:
    return json.dumps(normalize_result(data), sort_keys=True)
