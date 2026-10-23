import re
from typing import Dict, List

from google.cloud import secretmanager

from security_client import load_config


UNSAFE_PATTERNS = [r"password", r"token", r"private\s*key", r"secret"]


def secret_label_safety(secret_name: str) -> Dict[str, List[str]]:
    config = load_config()
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config.project_id}/secrets/{secret_name}"
    secret = client.get_secret(request={"name": name})
    findings = []
    for k, v in secret.labels.items():
        text = f"{k}={v}"
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in UNSAFE_PATTERNS):
            findings.append(text)
    return {"secret_name": secret_name, "unsafe_labels": findings}
