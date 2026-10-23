import boto3

from security_models import extract_json_secret, select_secret_value


def parse_json_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret_text = select_secret_value(response)
    return {"secret": extract_json_secret(secret_text, payload.get("key_field"))}
