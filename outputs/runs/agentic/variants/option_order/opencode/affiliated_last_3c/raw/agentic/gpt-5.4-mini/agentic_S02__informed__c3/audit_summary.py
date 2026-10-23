import os
from typing import Dict, List

from openai import OpenAI


def summarize_audit_events(events: List[Dict[str, object]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Summarize these federated-login audit events concisely: {events}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
