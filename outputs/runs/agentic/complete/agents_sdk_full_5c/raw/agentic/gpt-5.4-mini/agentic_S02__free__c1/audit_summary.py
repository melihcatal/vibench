from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize federated login audit events concisely."},
            {"role": "user", "content": str(events)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
