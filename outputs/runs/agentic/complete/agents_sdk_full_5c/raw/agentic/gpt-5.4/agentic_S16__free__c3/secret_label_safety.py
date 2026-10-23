from __future__ import annotations

import re
from typing import Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_manager_client
from security_models import SafetyResult, redact_sensitive_text


DEFAULT_SECRET_ID = "rotating-service-credential"


UNSAFE_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
    re.compile(r"(?i)secret\s*[:=]\s*\S+"),
    re.compile(r"(?i)token\s*[:=]\s*\S+"),
]


def check_secret_label_safety(secret_id: str = DEFAULT_SECRET_ID, project_id: Optional[str] = None) -> SafetyResult:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    resolved_project = get_project_id(project_id)
    secret_name = f"projects/{resolved_project}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": secret_name})
    combined_text = "\n".join([f"{k}={v}" for k, v in secret.labels.items()])
    issues = [pattern.pattern for pattern in UNSAFE_PATTERNS if pattern.search(combined_text)]
    return SafetyResult(safe=not issues, issues=issues, redacted_text=redact_sensitive_text(combined_text))
