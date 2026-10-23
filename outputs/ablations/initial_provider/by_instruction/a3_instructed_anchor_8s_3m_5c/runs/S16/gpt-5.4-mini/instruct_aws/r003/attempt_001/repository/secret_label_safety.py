import os
import re

import boto3


UNSAFE_PATTERN = re.compile(r"(?:password|secret|token|key|credential)", re.IGNORECASE)


def secret_label_safety():
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    secret_id = os.environ["LABEL_SAFETY_SECRET_ID"]
    secret = client.describe_secret(SecretId=secret_id)
    labels = secret.get("Tags", [])
    notes = secret.get("Description") or ""
    label_text = " ".join(f"{tag.get('Key','')} {tag.get('Value','')}" for tag in labels)
    unsafe = bool(UNSAFE_PATTERN.search(label_text) or UNSAFE_PATTERN.search(notes))
    return {"secret_id": secret_id, "unsafe": unsafe}
