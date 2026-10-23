import json
import os
from typing import Any, Mapping, Optional

import requests

OPENAI_COMPATIBLE_API_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.4-mini"


def _message_payload(message: Mapping[str, Any]) -> str:
    return json.dumps(message, ensure_ascii=False, separators=(",", ":"))


def send_to_dead_letter(message: Mapping[str, Any], destination: Optional[str] = None) -> dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    dead_letter_destination = destination or os.environ.get("OPENAI_DEAD_LETTER_DESTINATION", "dead-letter")
    response = requests.post(
        f"{OPENAI_COMPATIBLE_API_URL}/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEFAULT_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": "Route the failed message to the managed dead-letter destination.",
                },
                {
                    "role": "user",
                    "content": _message_payload({"destination": dead_letter_destination, "message": message}),
                },
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
