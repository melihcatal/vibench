import os
import openai


def fetch_api_key(secret_name: str = "my-api-key") -> str:
    """Fetch an API key from the Secure Secrets storage (OpenAI Secret Manager).

    Args:
        secret_name: Name of the secret to retrieve.

    Returns:
        The API key string.
    """
    # Configure OpenAI client to use the secret manager endpoint
    openai.api_base = os.getenv("SECRET_MANAGER_ENDPOINT")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resp = openai.SecretManager.get_secret(name=secret_name)
    return resp.secret
