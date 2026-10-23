from __future__ import annotations

import os
from typing import Any, Dict

from security_client import access_secret_text
from security_models import SecretRequest


def parse_json_secret(secret_id: str | None = None) -> Dict[str, Any]:
    request = SecretRequest(secret_id=secret_id or os.environ.get("JSON_SECRET_ID", "app-config"))
    secret = access_secret_text(request.secret_id, version=request.version)
    return secret.as_json_dict()
