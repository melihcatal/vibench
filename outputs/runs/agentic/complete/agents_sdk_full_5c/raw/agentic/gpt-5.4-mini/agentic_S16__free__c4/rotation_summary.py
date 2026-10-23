from __future__ import annotations

import os
from typing import Dict

from google.cloud import secretmanager

from security_client import get_gcp_project_id, secret_manager_client
from security_models import SecretAnalysisResponse


def summarize_rotation_status(project_id: str | None = None) -> SecretAnalysisResponse:
    client = secret_manager_client()
    parent = f"projects/{project_id or get_gcp_project_id()}"
    secrets = list(client.list_secrets(request={"parent": parent}))
    latest_count = 0
    for secret in secrets:
        if getattr(secret, "version_aliases", None):
            latest_count += 1
    summary = f"Found {len(secrets)} secrets; {latest_count} have version aliases configured."
    return SecretAnalysisResponse(risk_level="info", summary=summary, provider="google-cloud-secret-manager", metadata={"secret_count": len(secrets)})


if __name__ == "__main__":
    print(summarize_rotation_status().summary)
