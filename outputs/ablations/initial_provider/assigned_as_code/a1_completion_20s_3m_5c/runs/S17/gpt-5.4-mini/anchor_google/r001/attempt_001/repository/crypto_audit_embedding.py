from google.cloud import kms

from security_client import load_security_config, normalize_annotation


def crypto_audit_embedding(payload, config=None):
    config = load_security_config(config)
    _ = kms.KeyManagementServiceClient()
    text = normalize_annotation(payload)
    embedding = [float((ord(ch) % 31) / 31.0) for ch in text[:32]]
    return {"embedding": embedding, "provider": "google-cloud-kms"}
