import os

from security_client import get_secrets_client
from security_models import redact_text


def secret_label_safety(secret_id: str = None):
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_LABEL_ID", "labels/secret")
    response = client.describe_secret(SecretId=secret_id)
    labels = response.get("Tags", [])
    unsafe = []
    for item in labels:
        value = f"{item.get('Key', '')}:{item.get('Value', '')}"
        redacted = redact_text(value)
        if redacted != value:
            unsafe.append(value)
    note = response.get("Description", "")
    return {
        "secret_id": secret_id,
        "unsafe_labels": unsafe,
        "safe_note": redact_text(note),
    }
