from google.cloud import kms

from security_client import load_security_config, normalize_plaintext


def payload_safety(payload, config=None):
    config = load_security_config(config)
    _ = kms.KeyManagementServiceClient()
    text = normalize_plaintext(payload).decode("utf-8", errors="ignore").lower()
    unsafe = any(term in text for term in ("password", "secret", "ssn", "credit card"))
    return {"unsafe": unsafe}
