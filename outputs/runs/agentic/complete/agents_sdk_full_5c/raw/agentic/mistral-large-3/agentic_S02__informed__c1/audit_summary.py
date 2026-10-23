from openai import OpenAI
import os
import json
from typing import List, Dict


def summarize_audit_events(events: List[Dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the following federated login audit events in a concise report:\n"
        f"{json.dumps(events, indent=2)}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()