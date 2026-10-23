import re

from security_client import create_secret_client


def secret_label_safety(secret_name: str) -> bool:
    client = create_secret_client()
    secret = client.get_secret(secret_name)
    label = getattr(secret.properties, "tags", {}) or {}
    text = " ".join([secret_name, str(label), str(getattr(secret.properties, "content_type", ""))])
    return not bool(re.search(r"(?i)(password|token|secret|private key)", text))
