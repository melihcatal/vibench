from __future__ import annotations

from typing import Dict, List

from google.cloud import secretmanager

from security_client import build_secret_reference
from security_models import detect_unsafe_text, normalize_labels



def secret_label_safety(secret_id: str) -> List[Dict[str, str]]:
    ref = build_secret_reference(secret_id=secret_id)
    client = secretmanager.SecretManagerServiceClient()
    secret = client.get_secret(request={"name": f"projects/{ref.project_id}/secrets/{ref.secret_id}"})
    labels = normalize_labels(dict(secret.labels))
    note_text = getattr(secret, "annotations", {}).get("note", "") if getattr(secret, "annotations", None) else ""
    findings = detect_unsafe_text({**labels, "note": note_text})
    return [
        {
            "provider": "Google Cloud Secret Manager",
            "field_name": finding.field_name,
            "issue": finding.issue,
            "value": finding.value,
        }
        for finding in findings
    ]
