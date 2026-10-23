from __future__ import annotations

import os

from security_client import fetch_secret
from security_models import SecretRequest


def main() -> str:
    secret_name = os.environ.get("ROTATE_SECRET_NAME", "rotation-target")
    version_id = os.environ.get("ROTATE_SECRET_VERSION")
    version_stage = os.environ.get("ROTATE_SECRET_STAGE", "current")
    request = SecretRequest(secret_name=secret_name, version_id=version_id, version_stage=version_stage)
    return fetch_secret(request).value


if __name__ == "__main__":
    print(main())
