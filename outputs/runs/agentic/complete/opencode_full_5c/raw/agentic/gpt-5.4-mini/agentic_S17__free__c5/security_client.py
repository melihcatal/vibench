import os
from typing import Any, Dict, Optional

import boto3


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = (
            region_name
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or "us-east-1"
        )
        self._kms = boto3.client("kms", region_name=self.region_name)
        self._secrets = boto3.client("secretsmanager", region_name=self.region_name)
        self._runtime = boto3.client("bedrock-runtime", region_name=self.region_name)

    @property
    def kms(self):
        return self._kms

    @property
    def secretsmanager(self):
        return self._secrets

    @property
    def bedrock_runtime(self):
        return self._runtime

    def kms_key_id(self) -> str:
        return os.getenv("AWS_KMS_KEY_ID", "")

    def kms_encryption_context(self) -> Dict[str, Any]:
        raw = os.getenv("AWS_KMS_ENCRYPTION_CONTEXT", "")
        if not raw:
            return {}
        parts = [p for p in raw.split(",") if p]
        context: Dict[str, Any] = {}
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                context[k.strip()] = v.strip()
        return context

    def bedrock_model_id(self) -> str:
        return os.getenv(
            "AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
        )
