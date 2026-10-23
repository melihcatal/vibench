from __future__ import annotations

import os

from security_client import env_secret_version, safe_fetch


def rotate_secret_version(secret_id: str | None = None, *, version_id: str | None = None, version_stage: str | None = None) -> str:
    secret_name = secret_id or os.getenv("SECURITY_ROTATION_SECRET_ID", "rotation/secret")
    env_version_id, env_version_stage = env_secret_version()
    return safe_fetch(
        secret_name,
        version_id=version_id or env_version_id,
        version_stage=version_stage or env_version_stage,
    )
