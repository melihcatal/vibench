import os
from typing import Any, Dict

# General client configuration – keys can come from environment, shared config file, or Vault
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Example helper to load a JSON secret into a dict (wrapper around boto3 helper defined elsewhere)
# In practice you could import the earlier parse_json_secret function here


def load_aws_secret(secret_id: str) -> Dict[str, Any]:
    import json
    import boto3

    client = boto3.client(
        "secretsmanager",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    resp = client.get_secret_value(SecretId=secret_id)
    secret = resp.get("SecretString")
    if not secret:
        raise ValueError("Secret payload not found")
    return json.loads(secret)


# Centralised utility to validate secret labels against a blocklist (simple example)
BLOCKLIST = ["password", "token", "secret", "apikey"]


def check_secret_labels(labels: list) -> bool:
    """Return True if any label matches a blocked term."""
    return any(b in label.lower() for b in BLOCKLIST)
