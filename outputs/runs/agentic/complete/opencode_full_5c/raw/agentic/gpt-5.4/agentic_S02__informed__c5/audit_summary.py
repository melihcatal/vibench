from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditEvent


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    event_list: List[AuditEvent] = list(events)
    lines = [
        f"{event.occurred_at} | {event.provider} | {event.event_type} | user={event.user_id} | details={event.details}"
        for event in event_list
    ]
    prompt = (
        "Summarize these federated login audit events with key trends, anomalies, and user-impacting issues:\n"
        + "\n".join(lines)
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text
