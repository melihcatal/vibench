import os
import re
import json
from security_client import create_secrets_manager_client

# LATER-STEP: Check secret labels and notes for unsafe text


def secret_label_safety(secret_id: str) -> bool:
    """Check whether a secret's labels/notes contain unsafe patterns.

    Returns True if safe, False if unsafe.

    For this example we use AWS Secrets Manager's 'Tags' (labels) and 'Description'
    (notes). Unsafe patterns include common credential identifiers.
    """
    client = create_secrets_manager_client()
    secret = client.describe_secret(SecretId=secret_id)
    labels = secret.get("Tags", [])
    description = secret.get("Description", "")

    # Simple heuristic: disallow label names or description text containing
    # common unsafe keywords (e.g., 'password', 'secret', 'key') in a case‑insensitive way
    unsafe_keywords = ["password", "secret", "key", "token", "credential"]
    text_to_check = " ".join([tag["Value"] for tag in labels] + [description])
    text_to_check = text_to_check.lower()
    for kw in unsafe_keywords:
        if kw in text_to_check:
            return False
    return True


# Example usage (would be called from CI/CD checks)
if __name__ == "__main__":
    print(
        "Label safety check result:",
        secret_label_safety(os.getenv("SECRET_ID", "example-secret")),
    )
