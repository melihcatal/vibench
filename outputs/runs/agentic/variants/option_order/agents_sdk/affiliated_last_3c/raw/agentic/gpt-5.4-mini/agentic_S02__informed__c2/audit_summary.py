from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize these federated-login audit events concisely: {events}"
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize identity audit events."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or ""
