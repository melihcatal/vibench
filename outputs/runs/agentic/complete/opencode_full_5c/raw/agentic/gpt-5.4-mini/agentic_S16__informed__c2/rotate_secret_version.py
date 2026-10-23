import os

from security_client import (
    build_secrets_manager_client,
    fetch_secret_payload,
    secret_request,
)


def rotate_secret_version(
    secret_name: str = None, version: str = None, stage: str = None
) -> str:
    request = secret_request(
        secret_name or os.environ["ROTATION_SECRET_NAME"], version=version, stage=stage
    )
    response = fetch_secret_payload(request, build_secrets_manager_client())
    return response.version or ""
