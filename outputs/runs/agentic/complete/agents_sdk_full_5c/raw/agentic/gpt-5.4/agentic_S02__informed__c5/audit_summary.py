from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditRecord, AuditSummary


OPENAI_MODEL = "gpt-4o-mini"
PROVIDER = "OpenAI"



def summarize_federated_login_audit_events(events: Iterable[AuditRecord]) -> AuditSummary:
    event_list: List[AuditRecord] = list(events)
    successful = sum(1 for e in event_list if e.event_type == "login_success")
    failed = sum(1 for e in event_list if e.event_type == "login_failure")
    unique_users = len({e.user_id for e in event_list if e.user_id})
    ordered = sorted(event_list, key=lambda e: e.timestamp)
    period_start = ordered[0].timestamp if ordered else None
    period_end = ordered[-1].timestamp if ordered else None

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "provider": "Auth0",
        "counts": {
            "total_events": len(event_list),
            "successful_logins": successful,
            "failed_logins": failed,
            "unique_users": unique_users,
        },
        "events": [
            {
                "event_type": e.event_type,
                "user_id": e.user_id,
                "timestamp": e.timestamp,
                "details": e.details,
            }
            for e in event_list
        ],
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit activity concisely with risk observations.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    text = response.output_text
    return AuditSummary(
        provider=PROVIDER,
        total_events=len(event_list),
        successful_logins=successful,
        failed_logins=failed,
        unique_users=unique_users,
        period_start=period_start,
        period_end=period_end,
        generated_text=text,
        model=OPENAI_MODEL,
    )
