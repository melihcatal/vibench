import os
from typing import List, Dict
import anthropic

# Anthropic Messages API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def summarize_audit_events(audit_records: List[Dict]) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = (
        "Summarize the following federated login audit events in a concise report:\n"
        f"{audit_records}\n\n"
        "Include key metrics like total logins, unique users, and any anomalies."
    )
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text