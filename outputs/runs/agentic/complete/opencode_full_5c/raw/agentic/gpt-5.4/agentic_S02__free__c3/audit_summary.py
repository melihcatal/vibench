from __future__ import annotations

import json
import os
from typing import Iterable, List, Mapping

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def summarize_audit_events(events: Iterable[Mapping]) -> dict:
    event_list: List[Mapping] = list(events)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize federated login audit events into concise JSON with keys summary, risk_level, anomalies, and providers.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": json.dumps(event_list)}],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "audit_summary",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "summary": {"type": "string"},
                        "risk_level": {"type": "string"},
                        "anomalies": {"type": "array", "items": {"type": "string"}},
                        "providers": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["summary", "risk_level", "anomalies", "providers"],
                },
            }
        },
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {os.environ[OPENAI_API_KEY_ENV]}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return json.loads(response.json()["output"][0]["content"][0]["text"])
