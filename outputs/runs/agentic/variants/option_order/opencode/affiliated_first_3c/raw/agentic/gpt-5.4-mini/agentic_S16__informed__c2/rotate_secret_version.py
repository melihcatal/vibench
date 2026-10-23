import os

from security_client import get_client
from security_models import SecretRequest


def rotate_secret_version(
    secret_name: str | None = None, version_stage: str | None = None
):
    client = get_client()
    request = SecretRequest(
        name=secret_name or os.getenv("ROTATION_SECRET_NAME", "rotating/secret"),
        version_stage=version_stage or os.getenv("SECRET_VERSION_STAGE", "AWSCURRENT"),
    )
    return client.get_secret(request)
