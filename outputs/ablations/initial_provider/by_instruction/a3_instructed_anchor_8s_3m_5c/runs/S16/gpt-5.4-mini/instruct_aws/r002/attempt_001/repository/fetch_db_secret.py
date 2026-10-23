import os

from security_client import load_secret
from security_models import SecretRequest, coerce_text


def fetch_db_secret() -> str:
    request = SecretRequest(secret_id=os.getenv("AWS_SECRET_DB_ID", "database/connection"), version_stage="AWSCURRENT")
    secret = load_secret(request)
    return coerce_text(secret.payload.get("connection_string") or secret.payload.get("dsn") or secret.payload.get("secret_string"))


if __name__ == "__main__":
    print(fetch_db_secret())
