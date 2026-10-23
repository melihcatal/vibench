import os

from security_client import get_client
from security_models import SecretRequest


def rotate_secret_version(
    secret_name: str | None = None,
    version_id: str | None = None,
    stage: str | None = None,
):
    client = get_client()
    request = SecretRequest(
        secret_name=secret_name or os.environ["ROTATE_SECRET_NAME"],
        version_id=version_id,
        stage=stage,
    )
    return client.fetch(request).raw
