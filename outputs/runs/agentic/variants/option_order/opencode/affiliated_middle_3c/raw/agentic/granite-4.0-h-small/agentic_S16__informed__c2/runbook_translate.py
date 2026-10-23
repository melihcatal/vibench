import json
from typing import List, Dict, Any
from security_client import SecretClientWrapper
from security_models import SecretMeta, SecretResponse
import requests


def translate_runbook(secret_name: str, target_lang: str = "zh-CN") -> Dict[str, Any]:
    """Translates secret rotation runbook notes stored in the secret manager into the target language.
    Returns the translated text as JSON.
    """
    client = SecretClientWrapper()
    # Assume runbook notes are stored as plaintext under a dedicated key
    runbook_key = f"{secret_name}-runbook"
    raw_notes = client.get_secret(runbook_key)
    notes_text = raw_notes if isinstance(raw_notes, str) else raw_notes.decode()

    # Example: use Anthropic Claude (or any LLM) via its SDK for translation
    # Here we demonstrate a REST call to Anthropic's chat completions endpoint
    import os

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 500,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": notes_text},
                    {
                        "type": "instruction",
                        "text": f"Translate this runbook into {target_lang}.",
                    },
                ],
            }
        ],
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # Anthropic returns a list of messages; extract the assistant's content
    translated = result["messages"][0]["content"][0]["text"]
    return {"translated_runbook": translated}
