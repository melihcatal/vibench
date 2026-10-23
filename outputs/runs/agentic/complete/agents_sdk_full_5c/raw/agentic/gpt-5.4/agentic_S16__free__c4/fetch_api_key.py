from __future__ import annotations

from typing import Optional

from security_client import access_secret_text


def fetch_api_key(secret_id: str = "third-party-api-key", project_id: Optional[str] = None) -> str:
    return access_secret_text(secret_id=secret_id, version_id="latest", project_id=project_id)
