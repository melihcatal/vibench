# security_client.py
# Provides configuration helpers for secret management integrations.
import os
from typing import Optional

def get_iam_api_key() -> str:
    """Retrieve IAM API key from environment for IBM services."""
    return os.getenv("IBM_API_KEY")

def get_secret_crn(secret_type: str) -> str:
    """Map a logical secret type to its Cloud Resource Name (CRN)."
    mapping = {
        "api-key": os.getenv("API_KEY_CRN"),
        "db-connection": os.getenv("DB_SECRET_CRN"),
        "json-secret": os.getenv("JSON_SECRET_CRN")
    }
    return mapping.get(secret_type, "")

# AWS helpers

def get_access_key() -> str:
    """AWS Access Key ID from environment."""
    return os.getenv("AWS_ACCESS_KEY_ID")

def get_secret_access_key() -> str:
    """AWS Secret Access Key from environment."""
    return os.getenv("AWS_SECRET_ACCESS_KEY")

# Google Cloud helpers

def parse_google_credentials() -> Optional[dict]:
    """Parse a base64‑encoded Google service account JSON key from env."""
    encoded = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_B64")
    if not encoded:
        return None
    import base64, json
    decoded_bytes = base64.b64decode(encoded)
    return json.loads(decoded_bytes)

# Example utilities (can be expanded per secret store)

def resolve_secret_name(secret_type: str) -> str:
    """Resolve a friendly name to a concrete secret name."""
    mapping = {
        "api-key": os.getenv("API_KEY_NAME"),
        "db-connection": os.getenv("DB_SECRET_NAME"),
        "json-secret": os.getenv("JSON_SECRET_NAME")
    }
    return mapping.get(secret_type, "")
