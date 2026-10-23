from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def audit_summary(events: list[dict[str, Any]]) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "task": "summarize federated login audit events",
        "events": events,
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize login audit events with key risks and outcomes in JSON.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
