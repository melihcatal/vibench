from google.cloud import secretmanager

from security_client import load_config, secret_path, client
from security_models import safe_text


def audit_embedding() -> dict:
    config = load_config(secret_env="GOOGLE_AUDIT_SECRET_ID")
    secret = client().get_secret(request={"name": secret_path(config)})
    text = safe_text(f"{secret.name} {secret.labels} {getattr(secret, 'annotations', '') or ''}")
    return {"provider": "google-secret-manager", "text": text, "model": "text-embedding-004"}


if __name__ == "__main__":
    print(audit_embedding())
