import openai
import os
import json
from typing import List
from dataclasses import asdict
from identity_models import AuditEvent


def summarize_audit_events(events: List[AuditEvent]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    events_json = json.dumps([asdict(event) for event in events], indent=2)
    prompt = f"""Provide a concise summary of these federated login audit events in bullet points.
Include key stats (total events, unique users, success/failure rates), patterns, and any anomalies.

Events:
{events_json}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert security auditor for identity events.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()
