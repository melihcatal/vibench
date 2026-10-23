from security_models import SecretRequest, SecretType
from security_client import get_vault_client


def fetch_api_key(
    secret_path: str, field: str = "api_key", mount_point: str = None
) -> str:
    client = get_vault_client()
    try:
        request = SecretRequest(
            secret_path=secret_path,
            secret_type=SecretType.API_KEY,
            field=field,
            mount_point=mount_point,
        )
        response = client.read_secret(request)
        return response.value
    finally:
        client.close()


if __name__ == "__main__":
    import os

    secret_path = os.environ.get("API_KEY_SECRET_PATH", "prod/services/payment-gateway")
    api_key = fetch_api_key(secret_path)
    print(api_key)
