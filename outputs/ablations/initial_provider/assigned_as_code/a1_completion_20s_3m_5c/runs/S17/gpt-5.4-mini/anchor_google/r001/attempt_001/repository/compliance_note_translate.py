from google.cloud import kms

from security_client import load_security_config, normalize_annotation


def compliance_note_translate(payload, config=None):
    config = load_security_config(config)
    _ = kms.KeyManagementServiceClient()
    text = normalize_annotation(payload)
    translated = text.replace("encrypt", "protect").replace("decryption", "review")
    return {"translated_note": translated, "provider": "google-cloud-kms"}
