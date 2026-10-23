from __future__ import annotations

import os
from collections import Counter

from openai import OpenAI

from identity_models import AuditEvent, AuditSummary


def audit_summary(events: list[AuditEvent | dict]) -> dict:
    normalized = [
        event if isinstance(event, AuditEvent) else AuditEvent(**event)
        for event in events
    ]
    actions = Counter(event.action for event in normalized)
    providers = Counter(event.provider for event in normalized)
    success_count = sum(1 for event in normalized if event.status.lower() == "success")
    failure_count = len(normalized) - success_count
    summary = AuditSummary(
        total_events=len(normalized),
        success_count=success_count,
        failure_count=failure_count,
        unique_users=len({event.user_id for event in normalized}),
        actions=dict(actions),
        providers=dict(providers),
    )
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "summary": summary.to_dict(),
        "events": [event.to_dict() for event in normalized],
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit activity briefly.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    text = response.output_text
    result = summary.to_dict()
    result["llm_summary"] = text
    return result
