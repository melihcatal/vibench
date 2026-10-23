import boto3


def secret_label_safety(secret_id: str, region_name: str | None = None) -> dict:
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.describe_secret(SecretId=secret_id)
    name = response.get("Name", "")
    unsafe = any(token in name.lower() for token in ("tmp", "test", "unsafe", "debug"))
    return {"secret_id": secret_id, "unsafe": unsafe, "name": name}
