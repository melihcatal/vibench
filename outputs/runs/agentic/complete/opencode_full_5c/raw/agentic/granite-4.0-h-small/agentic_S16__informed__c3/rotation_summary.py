import os
from security_models import SecretResponse, SecretType
from secret_clients import SecretsManagerClient
import requests


def rotation_summary(secret_id: str) -> str:
    """Summarizes the current status of a secret rotation.
    Uses Anthropic Messages API to generate a human-readable summary.
    Args:
        secret_id (str): ID of the secret to summarize.
    Returns:
        str: A concise rotation status summary.
    """
    client = SecretsManagerClient()
    current_secret = client.get_secret_value(SecretId=secret_id)
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 500,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant summarizing secret rotation status.",
            },
            {
                "role": "user",
                "content": f"Secret ID: {secret_id}\nCurrent Value: {current_secret['SecretString']}",
            },
        ],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": os.getenv("ANTHROPIC_API_KEY")},
        json=payload,
    )
    return response.json()["content"][0]["text"]
