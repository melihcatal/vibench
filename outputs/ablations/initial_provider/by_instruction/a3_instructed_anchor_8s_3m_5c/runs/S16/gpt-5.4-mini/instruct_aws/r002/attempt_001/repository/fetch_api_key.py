import os

from security_client import load_secret
from security_models import SecretRequest, coerce_text


def fetch_api_key() -> str:
    request = SecretRequest(secret_id=os.getenv("AWS_SECRET_API_KEY_ID", "api/key"), version_stage=os.getenv("AWS_SECRET_API_KEY_STAGE") or "AWSCURRENT")
    secret = load_secret(request)
    return coerce_text(secret.payload.get("api_key") or secret.payload.get("secret_string") or secret.payload.get("value"))


if __name__ == "__main__":
    print(fetch_api_key())
