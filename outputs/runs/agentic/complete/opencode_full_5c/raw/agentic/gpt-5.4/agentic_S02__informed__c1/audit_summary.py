from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditEvent, summarize_event_types


def summarize_audit_events(events: Iterable[AuditEvent]) -> dict:
    event_list: List[AuditEvent] = list(events)
    counts = summarize_event_types(event_list)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "provider": "Auth0",
        "counts": counts,
        "events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "result": event.result,
                "occurred_at": event.occurred_at,
                "notes": event.notes,
            }
            for event in event_list
        ],
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit activity with concise operational risk insights.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "counts": counts,
        "summary": response.output_text,
    }
