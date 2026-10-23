import json

import boto3

from security_client import load_config, normalize_secret_value, secret_identifier


def parse_json_secret(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=secret_identifier(payload))
    value = normalize_secret_value(response)
    parsed = json.loads(value)
    if payload.get("field"):
        parsed = parsed[payload["field"]]
    return {"secret": parsed}
