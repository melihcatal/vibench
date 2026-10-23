import json

import boto3


def parse_json_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret_string = response["SecretString"]
    parsed_secret = json.loads(secret_string)
    return {"parsed_secret": parsed_secret}
