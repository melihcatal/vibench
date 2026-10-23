import re

import boto3


_UNSAFE = re.compile(r"(?i)(password|token|secret|apikey|api key|drop\s+table|rm\s+-rf)")


def is_label_safe(secret_id: str):
    client = boto3.client("secretsmanager")
    metadata = client.describe_secret(SecretId=secret_id)
    text = " ".join(filter(None, [metadata.get("Name", ""), metadata.get("Description", ""), str(metadata.get("Tags", ""))]))
    return not bool(_UNSAFE.search(text))
