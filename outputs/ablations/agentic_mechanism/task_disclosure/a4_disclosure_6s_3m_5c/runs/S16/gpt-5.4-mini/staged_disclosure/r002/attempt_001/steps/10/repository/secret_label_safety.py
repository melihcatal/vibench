import os
from typing import List, Dict, Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(secret_labels: List[str], notes: List[str]) -> str:
    labels = "\n".join(f"- {label}" for label in secret_labels)
    notes_text = "\n".join(f"- {note}" for note in notes)
    return (
        "Check the following secret labels and notes for unsafe text. "
        "Return JSON with keys unsafe (boolean), reasons (array of strings), and findings (array of objects with type, text, and reason).\n\n"
        f"Secret labels:\n{labels or '-'}\n\n"
        f"Notes:\n{notes_text or '-'}"
    )


def check_secret_labels_and_notes(secret_labels: List[str], notes: List[str]) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You analyze text for unsafe content."},
            {"role": "user", "content": _build_prompt(secret_labels, notes)},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        import json

        return json.loads(content)
    return content
