from __future__ import annotations

import os
import re
from typing import Iterable, List

from google.cloud import secretmanager

from security_models import normalize_text

_UNSAFE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in [r"password", r"token", r"secret", r"sudo", r"rm\s+-rf"]]


def check_secret_labels_and_notes(secret_id: str | None = None, project_id: str | None = None) -> List[str]:
    client = secretmanager.SecretManagerServiceClient()
    project = project_id or os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError("Missing GCP_PROJECT or GOOGLE_CLOUD_PROJECT")
    secret_id = secret_id or os.environ.get("LABEL_SAFETY_SECRET_ID", "rotation-target")
    name = f"projects/{project}/secrets/{normalize_text(secret_id)}"
    secret = client.get_secret(request={"name": name})
    findings: List[str] = []
    for label_value in getattr(secret, "labels", {}).values():
        if any(pattern.search(str(label_value)) for pattern in _UNSAFE_PATTERNS):
            findings.append(str(label_value))
    note = getattr(secret, "annotations", {}) if hasattr(secret, "annotations") else {}
    for value in note.values() if isinstance(note, dict) else []:
        if any(pattern.search(str(value)) for pattern in _UNSAFE_PATTERNS):
            findings.append(str(value))
    return findings
