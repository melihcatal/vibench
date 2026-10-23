from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_client, resolve_version_name
from security_models import ParsedJsonSecret, SecretValueResult


_PROVIDER = "google-cloud-secret-manager"


def parse_json_secret(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> ParsedJsonSecret:
    client = get_secret_client()
    project = project_id or get_project_id()
    name = resolve_version_name(project, secret_id, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    parsed: Dict[str, Any] = json.loads(payload)
    return ParsedJsonSecret.from_dict(SecretValueResult(provider=_PROVIDER, secret_id=secret_id, version=version, value=payload), parsed)


if __name__ == "__main__":
    secret_id = os.environ.get("SECRET_ID", "json-secret")
    secret = parse_json_secret(secret_id=secret_id, version=os.environ.get("SECRET_VERSION", "latest"))
    print(json.dumps(secret.data, sort_keys=True))
