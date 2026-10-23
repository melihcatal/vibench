from __future__ import annotations

from typing import Iterable

from google.cloud import secretmanager

from security_models import SafetyFinding, collect_unsafe_terms


DEFAULT_UNSAFE_TERMS = ("password", "secret", "token", "private key", "apikey")



def secret_label_safety(project_id: str, secret_id: str, extra_text: str = "", unsafe_terms: Iterable[str] = DEFAULT_UNSAFE_TERMS) -> SafetyFinding:
    client = secretmanager.SecretManagerServiceClient()
    secret = client.get_secret(request={"name": f"projects/{project_id}/secrets/{secret_id}"})
    label_blob = " ".join(f"{k}:{v}" for k, v in secret.labels.items())
    notes_blob = f"{secret.annotations if hasattr(secret, 'annotations') else ''} {extra_text}"
    text = f"{label_blob} {notes_blob}".strip()
    hits = collect_unsafe_terms(text, unsafe_terms)
    return SafetyFinding(text=text, unsafe_terms=hits, is_safe=not hits)
