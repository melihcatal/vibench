from typing import Optional
from security_models import SecretRequest, SecretType, parse_json_secret_value
from security_client import get_vault_client


def parse_json_secret(
    secret_path: str, field: Optional[str] = None, mount_point: Optional[str] = None
) -> dict:
    client = get_vault_client()
    try:
        request = SecretRequest(
            secret_path=secret_path,
            secret_type=SecretType.JSON_SECRET,
            field=field,
            mount_point=mount_point,
        )
        response = client.read_secret(request)
        return parse_json_secret_value(response.value)
    finally:
        client.close()


def get_json_secret_key(secret_path: str, key: str, mount_point: Optional[str] = None):
    data = parse_json_secret(secret_path, mount_point=mount_point)
    return data.get(key)


if __name__ == "__main__":
    import os

    secret_path = os.environ.get("JSON_SECRET_PATH", "prod/config/oauth-tokens")
    parsed = parse_json_secret(secret_path)
    print(parsed)
