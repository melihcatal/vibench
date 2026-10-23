import json
from security_client import get_secret_client
from security_models import SecretItem


def parse_json_secret(secret_name: str) -> dict:
    client = get_secret_client()
    try:
        secret = client.get_secret(secret_name)
        return json.loads(secret.value)
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve and parse JSON secret '{secret_name}': {e}"
        )
