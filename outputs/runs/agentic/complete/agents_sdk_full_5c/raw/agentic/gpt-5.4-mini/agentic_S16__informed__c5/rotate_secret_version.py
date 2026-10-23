from __future__ import annotations

from security_client import build_request, fetch_secret


def read_secret_version(secret_name: str, version_id: str | None = None, stage: str | None = "AWSCURRENT") -> str:
    response = fetch_secret(build_request(secret_name, version_id=version_id, stage=stage))
    return response.raw_value
