import os

import boto3


def secret_label_safety() -> bool:
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION"))
    secret_id = os.environ.get("SECRET_NAME", "secret-label")
    response = client.describe_secret(SecretId=secret_id)
    name = response.get("Name", "")
    description = response.get("Description", "")
    text = f"{name} {description}".lower()
    return not any(token in text for token in ("password", "token", "apikey", "secret"))
