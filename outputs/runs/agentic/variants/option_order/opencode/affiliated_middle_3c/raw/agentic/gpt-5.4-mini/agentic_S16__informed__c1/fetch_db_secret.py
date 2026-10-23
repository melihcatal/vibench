import os
from security_client import get_secret_value
from security_models import SecretRequest, ensure_mapping


def fetch_db_secret(secret_name: str | None = None) -> dict:
    request = SecretRequest(secret_name=secret_name or os.getenv("AWS_DB_SECRET_NAME", "db-connection"), version_stage=os.getenv("AWS_DB_SECRET_VERSION_STAGE", "AWSCURRENT"))
    return ensure_mapping(get_secret_value(request))
