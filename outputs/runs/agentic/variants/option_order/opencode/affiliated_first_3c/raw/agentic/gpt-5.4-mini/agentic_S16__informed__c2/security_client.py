import os
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_value


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = (
            region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        )
        self.client = boto3.client("secretsmanager", region_name=self.region_name)

    def get_secret(self, request: SecretRequest) -> SecretResponse:
        kwargs: Dict[str, Any] = {"SecretId": request.name}
        if request.version_stage:
            kwargs["VersionStage"] = request.version_stage
        result = self.client.get_secret_value(**kwargs)
        value = result.get("SecretString")
        if value is None and result.get("SecretBinary") is not None:
            value = result["SecretBinary"]
        return SecretResponse(
            name=request.name,
            value=normalize_secret_value(value),
            version_id=result.get("VersionId"),
            metadata={
                k: v
                for k, v in result.items()
                if k not in {"SecretString", "SecretBinary"}
            },
        )


def get_client() -> SecurityClient:
    return SecurityClient()
