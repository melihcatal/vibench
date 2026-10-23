from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditEvent


_OPENAI_MODEL = os.environ.get("OPENAI_AUDIT_MODEL", "gpt-4o-mini")


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    materialized: List[AuditEvent] = list(events)
    prompt = "\n".join(
        f"- time={event.occurred_at} provider={event.provider} type={event.event_type} actor={event.actor_subject} details={event.details}"
        for event in materialized
    )
    response = client.responses.create(
        model=_OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize federated-login audit activity, notable anomalies, and likely outcomes in concise operational prose.",
            },
            {
                "role": "user",
                "content": prompt or "No audit events provided.",
            },
        ],
    )
    return response.output_text
