import re

from security_client import get_secretsmanager_client


def secret_label_safety(payload, config=None):
    client = get_secretsmanager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    labels = json.loads(value).get("labels", [])
    unsafe_labels = [label for label in labels if re.search(r"[^a-zA-Z0-9_-]", label)]
    return {"unsafe_labels": unsafe_labels}