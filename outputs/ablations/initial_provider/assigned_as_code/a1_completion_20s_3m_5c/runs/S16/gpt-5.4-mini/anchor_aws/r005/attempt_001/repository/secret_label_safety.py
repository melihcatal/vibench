import boto3

from security_client import load_config


def secret_label_safety(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload["secret_id"])
    unsafe = []
    for value in list(response.get("Tags", [])) + [{"Key": "Description", "Value": response.get("Description", "")}]:
        text = (value.get("Value") or "").lower()
        if any(token in text for token in ["password", "secret", "token", "private key", "credential"]):
            unsafe.append(value)
    return {"unsafe": bool(unsafe), "matches": unsafe}
