import os
from typing import List
import openai
from identity_models import AuditEvent

def summarize_federated_login_audits(events: List[AuditEvent]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    event_str = "\n".join([f"{e.timestamp}: {e.user_id} - {e.event_type} {e.details}" for e in events])
    prompt = f"""Summarize these federated login audit events:

{event_str}

Provide a concise summary: total events, unique users, patterns, anomalies."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content