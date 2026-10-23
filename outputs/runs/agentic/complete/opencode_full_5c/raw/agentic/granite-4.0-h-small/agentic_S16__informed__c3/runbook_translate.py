import os
from secret_clients import SecretsManagerClient
import requests


def runbook_translate(secret_id: str, runbook_text: str) -> str:
    """Translates secret-rotation runbook notes into another language using DeepL API.
    Args:
        secret_id (str): ID of the secret associated with the runbook.
        runbook_text (str): Original English runbook content.
    Returns:
        str: Translated runbook text (e.g., Spanish).
    """
    client = SecretsManagerClient()
    # Dummy fetch to ensure secret exists (optional)
    client.get_secret_value(SecretId=secret_id)
    payload = {
        "text": runbook_text,
        "target_lang": "ES",  # Spanish translation
    }
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        auth=("YOUR_DEEPL_AUTH_KEY", ""),
        json=payload,
    )
    return response.json()["translations"][0]["text"]
