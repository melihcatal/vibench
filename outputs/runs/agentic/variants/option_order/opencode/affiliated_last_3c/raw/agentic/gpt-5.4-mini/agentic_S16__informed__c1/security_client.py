import os
from typing import Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_value


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = (
            region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        )
        self.client = boto3.client("secretsmanager", region_name=self.region_name)

    def fetch(self, request: SecretRequest) -> SecretResponse:
        kwargs = {"SecretId": request.secret_name}
        if request.version_id:
            kwargs["VersionId"] = request.version_id
        if request.stage:
            kwargs["VersionStage"] = request.stage
        payload = self.client.get_secret_value(**kwargs)
        return SecretResponse(
            name=request.secret_name,
            value=normalize_secret_value(
                payload.get("SecretString", payload.get("SecretBinary"))
            ),
            version_id=payload.get("VersionId"),
            raw=payload,
        )


def get_client() -> SecurityClient:
    return SecurityClient()
