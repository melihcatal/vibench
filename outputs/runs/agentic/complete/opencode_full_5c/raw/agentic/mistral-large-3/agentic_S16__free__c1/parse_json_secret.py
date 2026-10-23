from security_client import SecretManagerClient
from security_models import parse_json_secret


def parse_json_secret(secret_id: str = "SERVICE_CONFIG") -> dict:
    client = SecretManagerClient()
    secret_payload = client.get_secret_latest_version(secret_id)
    return parse_json_secret(secret_payload)
