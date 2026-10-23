from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import access_secret_payload


def parse_json_secret(secret_id: str = "application-config", version_id: str = "latest", project_id: Optional[str] = None) -> Dict[str, Any]:
    payload = access_secret_payload(secret_id=secret_id, version_id=version_id, project_id=project_id)
    return payload.json()
