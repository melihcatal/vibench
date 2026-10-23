import json
from security_client import get_secrets_client
from security_models import parse_json_secret


def retrieve_and_parse_json_secret(secret_name: str) -> dict:
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    return parse_json_secret(response["SecretString"])
