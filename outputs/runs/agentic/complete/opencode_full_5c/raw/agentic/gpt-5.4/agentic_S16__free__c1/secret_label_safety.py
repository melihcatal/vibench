from __future__ import annotations

import re

from google.cloud import secretmanager

from security_client import get_gcp_project_id, secret_manager_client
from security_models import SafetyCheckResult, normalize_labels


UNSAFE_PATTERNS = [
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret[_-]?value", re.IGNORECASE),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"private[_-]?key", re.IGNORECASE),
]


def check_secret_label_safety(
    secret_id: str, project_id: str | None = None
) -> SafetyCheckResult:
    project = get_gcp_project_id(project_id)
    client = secret_manager_client()
    name = f"projects/{project}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": name})
    labels = normalize_labels(secret.labels)
    notes = list(secret.annotations.items()) if hasattr(secret, "annotations") else []
    findings = []
    for key, value in {**labels, **dict(notes)}.items():
        text = f"{key}={value}"
        if any(pattern.search(text) for pattern in UNSAFE_PATTERNS):
            findings.append(text)
    return SafetyCheckResult(
        resource_name=secret.name, unsafe=bool(findings), findings=findings
    )
