from __future__ import annotations

from security_client import SecretManagerClientHelper
from security_models import SecretRequest, SecretResponse


def fetch_api_key(secret_name: str, version: str = "latest") -> SecretResponse:
    helper = SecretManagerClientHelper()
    request = SecretRequest(secret_name=secret_name, version=version)
    value = helper.access_secret(request.secret_name, request.version)
    return SecretResponse(secret_name=request.secret_name, version=request.version, value=value)
