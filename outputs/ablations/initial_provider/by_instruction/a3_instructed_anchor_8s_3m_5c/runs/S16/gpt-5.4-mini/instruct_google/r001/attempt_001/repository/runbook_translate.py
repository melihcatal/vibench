from google.cloud import secretmanager

from security_client import load_config, secret_path, client
from security_models import safe_text


def translate_runbook() -> dict:
    config = load_config(secret_env="GOOGLE_RUNBOOK_SECRET_ID")
    secret = client().get_secret(request={"name": secret_path(config)})
    return {"provider": "google-secret-manager", "text": safe_text(secret.name), "target_language": "en"}


if __name__ == "__main__":
    print(translate_runbook())
