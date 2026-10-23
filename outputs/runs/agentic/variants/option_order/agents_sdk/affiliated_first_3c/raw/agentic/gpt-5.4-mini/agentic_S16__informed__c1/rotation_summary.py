from __future__ import annotations

import os
from typing import Dict

from google.cloud import secretmanager

from security_models import normalize_text


def summarize_rotation(project_id: str | None = None, secret_id: str | None = None) -> Dict[str, str]:
    client = secretmanager.SecretManagerServiceClient()
    project = project_id or os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError("Missing GCP_PROJECT or GOOGLE_CLOUD_PROJECT")
    if not secret_id:
        secret_id = os.environ.get("ROTATION_SUMMARY_SECRET_ID", "rotation-target")
    parent = f"projects/{project}/secrets/{normalize_text(secret_id)}"
    secret = client.get_secret(request={"name": parent})
    return {
        "name": secret.name,
        "rotation": str(secret.rotation),
        "replication": str(secret.replication),
        "etag": str(secret.etag),
    }
