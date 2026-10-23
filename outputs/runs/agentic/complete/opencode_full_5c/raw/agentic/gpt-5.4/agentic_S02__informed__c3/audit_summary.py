from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def summarize_audit_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit events with concise risk-focused output.",
            },
            {
                "role": "user",
                "content": f"Audit events: {events}",
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
