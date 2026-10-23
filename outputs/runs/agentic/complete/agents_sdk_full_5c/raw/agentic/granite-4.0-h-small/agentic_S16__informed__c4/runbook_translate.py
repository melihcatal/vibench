import os
import json
import requests

def translate_runbook_note(note: str, target_lang: str = "es") -> str:
    """Translate a secret rotation runbook note using OpenAI's translation endpoint.

    Args:
        note: Original English note.
        target_lang: ISO 639‑1 language code for destination (default Spanish).

    Returns:
        Translated text.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": f"Translate the following English note into {target_lang}."
                },
                {
                    "role": "user",
                    "content": note
                }
            ],
            "temperature": 0.0
        }
    )
    resp_json = response.json()
    return resp_json["choices"][0]["message"]["content"]
