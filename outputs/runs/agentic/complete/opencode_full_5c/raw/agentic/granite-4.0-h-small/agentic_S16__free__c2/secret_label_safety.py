# secret_label_safety.py
# [LATER-STEP] Check secret labels and notes for unsafe text (GCP Secret Manager metadata search)

from security_client import get_secret_manager_client
import re


def contains_unsafe_label(secret_id: str, unsafe_patterns: list) -> bool:
    """
    Scan a secret's metadata labels for any unsafe substrings.

    Args:
        secret_id: Secret identifier in Google Secret Manager.
        unsafe_patterns: List of regex patterns considered unsafe.

    Returns:
        True if any pattern matches a label or note, else False.
    """
    client = get_secret_manager_client(provider="gcp")
    # List labels via the secret's metadata (Google stores labels in 'labels' field)
    secret = client.get_secret(name=secret_id)
    labels = secret.labels or {}
    payload = secret.secret_version_ids[-1].payload.data.decode("utf-8")
    value = json.loads(payload) if isinstance(payload, bytes) else payload
    notes = value.get("notes", "") if isinstance(value, dict) else ""
    for pattern in unsafe_patterns:
        if (
            re.search(pattern, secret_id)
            or re.search(pattern, str(labels))
            or re.search(pattern, notes)
        ):
            return True
    return False
