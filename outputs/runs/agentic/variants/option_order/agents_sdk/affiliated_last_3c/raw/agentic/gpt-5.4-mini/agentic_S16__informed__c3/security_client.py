from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import NormalizedSecret, SecretRequest, normalize_secret_payload


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.client = boto3.client("secretsmanager", region_name=self.region_name)

    def get_secret(self, request: SecretRequest) -> NormalizedSecret:
        kwargs: Dict[str, Any] = {"SecretId": request.name}
        if request.version_id:
            kwargs["VersionId"] = request.version_id
        if request.stage:
            kwargs["VersionStage"] = request.stage
        try:
            response = self.client.get_secret_value(**kwargs)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"AWS Secrets Manager lookup failed for {request.name}: {exc}") from exc

        payload = {"secret_string": response.get("SecretString", ""), **response}
        return normalize_secret_payload(request.name, payload)

    def get_secret_text(self, request: SecretRequest) -> str:
        return self.get_secret(request).value

    def get_json_secret(self, request: SecretRequest) -> Dict[str, Any]:
        secret_text = self.get_secret_text(request)
        try:
            return json.loads(secret_text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Secret {request.name} does not contain valid JSON") from exc
