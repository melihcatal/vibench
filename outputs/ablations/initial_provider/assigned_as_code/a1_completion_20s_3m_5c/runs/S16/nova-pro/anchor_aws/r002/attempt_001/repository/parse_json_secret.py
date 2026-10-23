import json
import boto3

def parse_json_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    parsed_value = json.loads(value)
    return parsed_value