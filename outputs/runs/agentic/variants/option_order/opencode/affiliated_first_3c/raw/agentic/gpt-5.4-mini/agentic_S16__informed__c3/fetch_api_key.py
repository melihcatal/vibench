from security_client import create_secrets_manager_client, get_secret_name
from security_models import normalize_secret_value


def fetch_api_key() -> str:
    client = create_secrets_manager_client()
    secret_id = get_secret_name("api-key")
    response = client.get_secret_value(SecretId=secret_id)
    return normalize_secret_value(
        response.get("SecretString") or response.get("SecretBinary")
    )
