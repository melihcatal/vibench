import boto3
from security_models import SecretRequest


def secret_label_safety(secret_id: str) -> dict:
    client = boto3.client("secretsmanager")
    request = SecretRequest(secret_id=secret_id)
    metadata = client.describe_secret(SecretId=request.secret_id)
    name = metadata.get("Name", "")
    description = metadata.get("Description", "") or ""
    unsafe = any(token in f"{name} {description}".lower() for token in ["password", "token", "private key", "secret"])
    return {"secret_id": request.secret_id, "unsafe": unsafe, "name": name}
