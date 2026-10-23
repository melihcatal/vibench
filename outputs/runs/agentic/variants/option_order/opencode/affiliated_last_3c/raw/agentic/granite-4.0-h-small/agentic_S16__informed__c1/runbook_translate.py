import os
import json
import requests
from security_models import SecretRequest, normalize_response


def runbook_translate(request: SecretRequest) -> str:
    """Translate secret-rotation runbook notes using Anthropic model.

    Returns the translated text.
    """
    secret_name = request["name"]
    runbook_note = f"Runbook for rotating secret {secret_name} has steps: ..."
    headers = {
        "Authorization": f"Bearer {os.getenv('ANTHROPIC_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "messages": [{"role": "user", "content": runbook_note}],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=payload
    )
    response.raise_for_status()
    result = response.json()
    return result["content"][0]["text"]
