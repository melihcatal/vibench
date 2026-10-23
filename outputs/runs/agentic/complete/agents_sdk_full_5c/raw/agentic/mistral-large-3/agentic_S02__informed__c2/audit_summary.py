from openai import OpenAI
import os
from typing import List, Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    prompt = (
        "Summarize the following federated login audit events in a concise report:\n"
        f"{events}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()