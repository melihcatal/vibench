import os
from typing import List
from openai import OpenAI
from identity_models import AuditEvent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_federated_login_audits(events: List[AuditEvent]) -> str:
    event_str = "\\n".join(
        [
            f"{e['timestamp']}: {e['event_type']} (user: {e.get('user_id', 'N/A')}, success: {e['success']})"
            for e in events
        ]
    )
    prompt = f"""Summarize the federated login audit events below in 2-3 sentences, highlighting key patterns, anomalies, and overall login success rate:

{event_str}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a security auditor."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content
