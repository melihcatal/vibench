from security_client import get_secret_client
from security_models import SecretItem


def rotate_secret_version(secret_name: str, secret_version: str) -> SecretItem:
    client = get_secret_client()
    try:
        secret = client.get_secret(secret_name, version=secret_version)
        return SecretItem(
            name=secret.name, value=secret.value, version=secret.id.split("/")[-1]
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to read secret '{secret_name}' with version '{secret_version}': {e}"
        )
