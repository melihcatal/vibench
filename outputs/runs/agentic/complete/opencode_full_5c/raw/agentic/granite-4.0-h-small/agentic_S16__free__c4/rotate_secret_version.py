import os
import openai


def rotate_secret_version(secret_name: str = "api-key", version: int = 2) -> str:
    """Read a specific version or staged value of a secret.

    Args:
        secret_name: Name of the secret.
        version: Version number or staged marker (e.g., 'staging').

    Returns:
        The requested secret value.
    """
    openai.api_base = os.getenv("SECRET_MANAGER_ENDPOINT")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resp = openai.SecretManager.get_secret_version(name=secret_name, version=version)
    return resp.secret
