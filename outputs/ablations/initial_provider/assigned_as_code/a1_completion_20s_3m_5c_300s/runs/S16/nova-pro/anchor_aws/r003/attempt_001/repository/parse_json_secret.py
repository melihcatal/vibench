import json

from security_client import get_secretsmanager_client


def parse_json_secret(payload, config=None):
    client = get_secretsmanager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    parsed_value = json.loads(value)
    return parsed_value