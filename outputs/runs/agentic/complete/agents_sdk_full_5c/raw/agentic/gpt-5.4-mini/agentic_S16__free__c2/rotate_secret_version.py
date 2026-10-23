from __future__ import annotations

import os
from typing import Optional

from security_client import get_secret_value
from security_models import normalize_secret_value

AWS_SECRET_ID = os.getenv("ROTATION_SECRET_ID", "prod/rotating-secret")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
VERSION_STAGE = os.getenv("SECRET_VERSION_STAGE", "AWSPREVIOUS")
VERSION_ID = os.getenv("SECRET_VERSION_ID")


def read_secret_version(version_stage: Optional[str] = VERSION_STAGE, version_id: Optional[str] = VERSION_ID) -> str:
    payload = get_secret_value(AWS_SECRET_ID, region_name=AWS_REGION, version_stage=version_stage, version_id=version_id)
    secret = normalize_secret_value(AWS_SECRET_ID, payload)
    return secret.as_text()
