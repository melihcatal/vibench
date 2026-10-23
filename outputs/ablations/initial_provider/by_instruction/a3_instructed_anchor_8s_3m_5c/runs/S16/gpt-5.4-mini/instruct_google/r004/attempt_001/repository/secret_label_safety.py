from google.cloud import secretmanager

from security_client import build_client, load_config
from security_models import normalize_label_text


def secret_label_safety(secret_id: str = "labeled-secret") -> bool:
    config = load_config(secret_id)
    client: secretmanager.SecretManagerServiceClient = build_client()
    secret = client.get_secret(request={"name": f"projects/{config.project_id}/secrets/{config.secret_id}"})
    label_text = normalize_label_text(" ".join(f"{k}:{v}" for k, v in secret.labels.items()))
    notes = normalize_label_text(secret.annotations.get("notes") if hasattr(secret, "annotations") and secret.annotations else None)
    return not any(token in f"{label_text} {notes}".lower() for token in ("password", "token", "secret", "unsafe"))
