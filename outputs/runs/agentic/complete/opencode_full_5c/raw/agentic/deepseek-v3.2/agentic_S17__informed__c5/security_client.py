import os
import json
import base64
from typing import Dict, Any, Optional, Union
import boto3
from botocore.exceptions import ClientError


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.kms_client = boto3.client("kms", region_name=self.region_name)

    def get_key_id(self, key_alias: Optional[str] = None) -> str:
        if key_alias:
            if not key_alias.startswith("alias/"):
                key_alias = f"alias/{key_alias}"
            return key_alias
        return os.getenv("AWS_KMS_KEY_ID", "")

    def validate_key_id(self, key_id: str) -> bool:
        if not key_id:
            return False
        try:
            self.kms_client.describe_key(KeyId=key_id)
            return True
        except ClientError:
            return False

    def encode_payload(self, payload: Union[str, bytes, Dict[str, Any]]) -> bytes:
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode("utf-8")
        elif isinstance(payload, str):
            payload = payload.encode("utf-8")
        return payload

    def decode_payload(self, payload: bytes) -> Union[str, Dict[str, Any]]:
        try:
            decoded = payload.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return payload.decode("utf-8", errors="ignore")

    def base64_encode(self, data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    def base64_decode(self, data: str) -> bytes:
        return base64.b64decode(data)

    def get_client_info(self) -> Dict[str, Any]:
        return {
            "provider": "AWS KMS",
            "region": self.region_name,
            "client_type": "boto3.kms",
            "auth_method": "AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY",
        }
