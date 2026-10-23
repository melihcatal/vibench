import os
from security_client import get_secret_value
from security_models import SecretRequest


def fetch_api_key(secret_name: str | None = None) -> str:
    request = SecretRequest(secret_name=secret_name or os.getenv("AWS_SECRET_NAME", "api-key"), version_stage=os.getenv("AWS_SECRET_VERSION_STAGE", "AWSCURRENT"))
    return get_secret_value(request)
