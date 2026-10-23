import json

from security_client import create_secret_client
from security_models import SecretRequest, normalize_secret_payload


def parse_json_secret(secret_name: str):
    client = create_secret_client()
    request = SecretRequest(name=secret_name)
    secret = client.get_secret(request.name)
    data = normalize_secret_payload(secret)
    return json.loads(data["value"])
