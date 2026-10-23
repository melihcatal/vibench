from __future__ import annotations

from typing import Dict

from security_client import SecretManagerClientHelper
from security_models import SecretRequest, normalize_secret_value


def fetch_db_secret(secret_name: str, version: str = "latest") -> Dict[str, str]:
    helper = SecretManagerClientHelper()
    request = SecretRequest(secret_name=secret_name, version=version)
    secret_text = helper.access_secret(request.secret_name, request.version)
    return {
        "connection_string": normalize_secret_value(secret_text),
        "provider": "google-cloud-secret-manager",
        "version": request.version,
    }
