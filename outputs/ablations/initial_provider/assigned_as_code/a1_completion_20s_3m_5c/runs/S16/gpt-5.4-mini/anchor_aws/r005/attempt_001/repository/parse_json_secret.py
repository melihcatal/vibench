import boto3

from security_client import load_config, secret_string
from security_models import parse_json_secret as decode_secret, select_field


def parse_json_secret(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret = decode_secret(secret_string(response))
    return {"secret": select_field(secret, payload.get("field"))}
