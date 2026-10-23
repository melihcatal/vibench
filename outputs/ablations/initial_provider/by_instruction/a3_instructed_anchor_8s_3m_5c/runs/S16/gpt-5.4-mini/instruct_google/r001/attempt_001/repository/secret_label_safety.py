from google.cloud import secretmanager

from security_client import load_config, secret_path, client
from security_models import safe_text


def label_safety() -> dict:
    config = load_config(secret_env="GOOGLE_LABEL_SECRET_ID")
    secret = client().get_secret(request={"name": secret_path(config)})
    labels = {k: safe_text(v) for k, v in secret.labels.items()}
    notes = safe_text(getattr(secret, "annotations", "") or "")
    unsafe = any(token in f"{labels} {notes}".lower() for token in ["password", "secret", "token", "key"])
    return {"safe": not unsafe, "labels": labels, "notes": notes}


if __name__ == "__main__":
    print(label_safety())
