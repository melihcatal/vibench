import os
from typing import Any, Dict, List

import openai


def audit_summary(events: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize these federated-login audit events in one paragraph: {events}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
