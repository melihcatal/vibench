import os
import re

import boto3


UNSAFE_PATTERNS = [re.compile(pattern, re.I) for pattern in [r"password", r"ssn", r"credit\s*card", r"secret"]]


def secret_label_safety():
    client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    secret_id = os.getenv("AWS_LABEL_SAFETY_SECRET_ID", "labels/secret")
    metadata = client.describe_secret(SecretId=secret_id)
    labels = metadata.get("Tags", [])
    notes = metadata.get("Description", "")
    text = " ".join([str(item.get("Value", "")) for item in labels] + [notes])
    unsafe = any(pattern.search(text) for pattern in UNSAFE_PATTERNS)
    return {"secret_id": secret_id, "unsafe": unsafe, "labels": labels, "notes": notes}


if __name__ == "__main__":
    print(secret_label_safety())
