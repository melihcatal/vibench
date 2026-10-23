from __future__ import annotations

from google.cloud import secretmanager

from security_client import get_secret_metadata
from security_models import normalize_labels, normalize_text


UNSAFE_TERMS = {"password", "secret", "token", "private_key", "credential"}


def secret_label_safety(secret_id: str, notes: str | None = None) -> dict[str, object]:
    secret: secretmanager.Secret = get_secret_metadata(secret_id)
    labels = normalize_labels(secret.labels)
    note_text = normalize_text(notes)
    joined = " ".join(list(labels.keys()) + list(labels.values()) + [note_text]).lower()
    findings = sorted(term for term in UNSAFE_TERMS if term in joined)
    return {
        "secret_name": secret.name,
        "unsafe": bool(findings),
        "findings": findings,
        "labels": labels,
    }
