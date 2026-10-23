import os
from security_client import get_secret_value
from security_models import SecretRequest


def rotate_secret_version(secret_name: str | None = None, version_stage: str | None = None) -> str:
    request = SecretRequest(secret_name=secret_name or os.getenv("AWS_ROTATE_SECRET_NAME", "rotating-secret"), version_stage=version_stage or os.getenv("AWS_ROTATE_SECRET_VERSION_STAGE", "AWSPREVIOUS"))
    return get_secret_value(request)
