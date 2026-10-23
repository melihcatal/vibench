from __future__ import annotations

import os
import re
from typing import List

import boto3

from security_client import load_security_client_config

UNSAFE_PATTERN = re.compile(r"(?i)(password|secret|token|drop\s+table|rm\s+-rf)")


def check_secret_labels_and_notes(secret_id: str) -> List[str]:
    client = boto3.client("secretsmanager", **load_security_client_config().__dict__)
    resp = client.describe_secret(SecretId=secret_id)
    findings: List[str] = []
    for label in resp.get("Tags", []):
        text = f"{label.get('Key', '')}={label.get('Value', '')}"
        if UNSAFE_PATTERN.search(text):
            findings.append(text)
    note = resp.get("Description", "")
    if note and UNSAFE_PATTERN.search(note):
        findings.append(note)
    return findings


if __name__ == "__main__":
    print(check_secret_labels_and_notes(os.getenv("SAFE_LABEL_SECRET_ID", "")))
