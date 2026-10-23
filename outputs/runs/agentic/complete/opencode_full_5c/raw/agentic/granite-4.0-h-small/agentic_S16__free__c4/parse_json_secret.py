import json
import os
import openai


def parse_json_secret(secret_name: str = "config-json") -> dict:
    """Retrieve a JSON-formatted secret and return it as a dict.

    Args:
        secret_name: Name of the secret to retrieve.

    Returns:
        Parsed JSON object (dict). Raises ValueError if invalid JSON.
    """
    openai.api_base = os.getenv("SECRET_MANAGER_ENDPOINT")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resp = openai.SecretManager.get_secret(name=secret_name)
    raw = resp.secret
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Secret {secret_name} is not valid JSON") from exc
