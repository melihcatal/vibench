import re

from security_client import get_secrets_client


def secret_label_safety(payload, config=None):
    client = get_secrets_client(config)
    response = client.describe_secret(SecretId=payload["secret_id"])
    labels = response["Name"] + " " + response["Description"]
    unsafe_patterns = ["password", "secret", "key"]
    is_safe = all(pattern not in labels.lower() for pattern in unsafe_patterns)
    return {"is_safe": is_safe}