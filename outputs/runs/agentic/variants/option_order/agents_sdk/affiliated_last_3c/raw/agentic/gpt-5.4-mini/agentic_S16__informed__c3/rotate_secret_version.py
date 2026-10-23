from __future__ import annotations

from typing import Optional

from security_client import SecurityClient
from security_models import SecretRequest

AWS_ROTATION_SECRET_NAME = "prod/rotating/secret"


def rotate_secret_version(secret_name: str = AWS_ROTATION_SECRET_NAME, version_id: Optional[str] = None, stage: Optional[str] = "AWSCURRENT") -> str:
    client = SecurityClient()
    return client.get_secret_text(SecretRequest(name=secret_name, version_id=version_id, stage=stage))
