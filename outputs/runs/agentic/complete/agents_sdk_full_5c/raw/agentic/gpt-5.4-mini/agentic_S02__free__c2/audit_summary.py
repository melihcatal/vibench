from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def audit_summary(events: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize federated-login audit events."},
            {"role": "user", "content": str(events)},
        ],
    )
    return response.output_text
