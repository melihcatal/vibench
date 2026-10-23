from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def summarize_audit_events(events: list[Dict[str, Any]]) -> str:
    prompt = "Summarize the federated-login audit events with risks, anomalies, and notable identity-provider patterns."
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": prompt + "\n" + str(events)}],
    )
    return response.output_text
