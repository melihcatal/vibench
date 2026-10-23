from typing import Dict

from google.cloud import dlp_v2

from security_models import normalize_text


def payload_safety(payload: str) -> Dict[str, bool]:
    client = dlp_v2.DlpServiceClient()
    _ = client
    text = normalize_text(payload).lower()
    return {"safe": not any(token in text for token in ("password", "secret", "private key", "ssn"))}
