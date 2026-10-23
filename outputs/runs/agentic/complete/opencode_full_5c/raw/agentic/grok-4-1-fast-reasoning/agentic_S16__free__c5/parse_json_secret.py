import json
from security_client import SecurityClient
from security_models import SecretResponse


def parse_json_secret(secret_name: str = "prod/json-secret") -> dict:
    client = SecurityClient()
    response: SecretResponse = client.get_secret(secret_name)
    return json.loads(response.value)
