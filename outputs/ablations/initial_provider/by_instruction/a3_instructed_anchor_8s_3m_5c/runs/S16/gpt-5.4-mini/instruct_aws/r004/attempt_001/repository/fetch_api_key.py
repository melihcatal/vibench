from security_client import load_secret_name, secrets_manager_client
from security_models import normalize_secret_payload


def fetch_api_key(secret_name: str = None) -> str:
    client = secrets_manager_client()
    secret_id = secret_name or load_secret_name("api/key")
    response = client.get_secret_value(SecretId=secret_id)
    normalized = normalize_secret_payload(response)
    return normalized["value"]


if __name__ == "__main__":
    print(fetch_api_key())
