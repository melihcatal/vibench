import boto3

from security_models import NormalizePayload, NormalizeResponse


def fetch_db_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    normalized_value = NormalizePayload(value)
    return NormalizeResponse({"db_secret": normalized_value})