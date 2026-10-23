import os
import hvac
from security_client import get_hvac_client
from security_models import SecretValue


def rotate_secret_version(secret_path: str, version: int) -> SecretValue:
    client = get_hvac_client()

    if not client.is_authenticated():
        raise ConnectionError("Vault client is not authenticated.")

    try:
        # In Vault, reading a secret path with a specific version
        secret_version_response = client.secrets.kv.v2.read_secret_version(
            path=secret_path,
            version=version,
        )
    except hvac.exceptions.InvalidPath:
        print(f"Secret path '{secret_path}' not found.")
        raise
    except Exception as e:
        print(f"Error reading secret version: {e}")
        raise

    secret_data = secret_version_response["data"]["data"]

    return SecretValue(
        secret_id=secret_path,
        secret_string=str(secret_data),
        version_id=str(secret_version_response["data"]["metadata"]["version"]),
    )


if __name__ == "__main__":
    vault_secret_path = os.environ.get("VAULT_SECRET_PATH", "my/kv/secret")
    secret_version_to_fetch = int(os.environ.get("VAULT_SECRET_VERSION", 1))
    try:
        secret = rotate_secret_version(vault_secret_path, secret_version_to_fetch)
        print(f"Fetched secret version {secret.version_id} for path {secret.secret_id}")
    except (ValueError, ConnectionError) as e:
        print(
            f"Could not fetch secret. Check logs and environment variables (VAULT_ADDR, VAULT_TOKEN). Error: {e}"
        )
