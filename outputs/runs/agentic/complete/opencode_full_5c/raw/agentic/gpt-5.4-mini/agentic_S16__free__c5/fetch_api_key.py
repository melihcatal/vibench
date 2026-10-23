from security_client import secret_manager_client, secret_version_path
from security_models import decode_secret_bytes


def fetch_api_key(secret_id: str = "api-key") -> str:
    client = secret_manager_client()
    response = client.access_secret_version(
        request={"name": secret_version_path(secret_id)}
    )
    return decode_secret_bytes(response.payload.data)
