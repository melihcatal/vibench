# Federated Login Flow - Audit Summary

import os
import json
from typing import Dict, List
from identity_models import AuditEvent
from openai import OpenAI


def audit_summary(events: List[AuditEvent]) -> str:
    """Summarize federated-login audit events using OpenAI GPT-4."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    event_texts = []
    for event in events:
        event_text = (
            f"Event ID: {event.event_id}\n"
            f"Timestamp: {event.timestamp}\n"
            f"User ID: {event.user_id}\n"
            f"Provider: {event.provider}\n"
            f"Action: {event.action}\n"
            f"Metadata: {json.dumps(event.metadata)}\n"
            f"IP Address: {event.ip_address or 'N/A'}\n"
            f"User Agent: {event.user_agent or 'N/A'}\n"
        )
        event_texts.append(event_text)

    prompt = (
        "Summarize the following federated-login audit events in a concise report:\n"
        f"{'=' * 50}\n"
        f"{chr(10).join(event_texts)}\n"
        f"{'=' * 50}\n"
        "Include key metrics, anomalies, and security observations."
    )

    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content
