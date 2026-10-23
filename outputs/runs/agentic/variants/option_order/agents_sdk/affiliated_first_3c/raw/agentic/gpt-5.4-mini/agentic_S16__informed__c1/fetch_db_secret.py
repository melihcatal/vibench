from __future__ import annotations

import os
from typing import Dict

from security_client import access_secret_dict, access_secret_text
from security_models import SecretRequest


def fetch_db_secret(secret_id: str | None = None) -> Dict[str, str]:
    request = SecretRequest(secret_id=secret_id or os.environ.get("DB_SECRET_ID", "database-connection"))
    return access_secret_dict(request.secret_id, version=request.version)


def fetch_db_uri(secret_id: str | None = None) -> str:
    request = SecretRequest(secret_id=secret_id or os.environ.get("DB_SECRET_ID", "database-connection"))
    return access_secret_text(request.secret_id, version=request.version).value
