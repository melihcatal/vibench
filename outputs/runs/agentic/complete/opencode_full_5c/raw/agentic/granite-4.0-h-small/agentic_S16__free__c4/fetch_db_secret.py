import os
import openai


def fetch_db_secret(secret_name: str = "db-credentials") -> dict:
    """Fetch a database connection secret from the Secure Secrets storage (OpenAI Secret Manager).

    Args:
        secret_name: Name of the secret to retrieve.

    Returns:
        A dictionary containing DB connection details.
    """
    openai.api_base = os.getenv("SECRET_MANAGER_ENDPOINT")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resp = openai.SecretManager.get_secret(name=secret_name)
    return resp.secret  # expected to be a JSON string or dict
