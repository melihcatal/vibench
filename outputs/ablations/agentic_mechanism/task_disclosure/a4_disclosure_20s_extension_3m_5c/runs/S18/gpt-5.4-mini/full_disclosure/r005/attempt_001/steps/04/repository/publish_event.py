import json
import os
from typing import Any, Mapping, Optional

import requests

OPENAI_COMPATIBLE_API_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.4-mini"


def _event_payload(event: Mapping[str, Any]) -> str:
    return json.dumps(event, ensure_ascii=False, separators=(",", ":"))


def publish_event(event: Mapping[str, Any], topic: Optional[str] = None) -> dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    target_topic = topic or os.environ.get("OPENAI_MESSAGING_TOPIC", "default")
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
                    "content": "Publish the provided JSON event to the managed messaging topic."
                },
                {
                    "role": "user",
                    "content": _event_payload({"topic": target_topic, "event": event}),
                },
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
