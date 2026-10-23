from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

from identity_models import summarize_audit_events


def summarize_federated_login_audit(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    local_summary = summarize_audit_events(events)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "events": events,
        "local_summary": {
            "total_events": local_summary.total_events,
            "success_count": local_summary.success_count,
            "failure_count": local_summary.failure_count,
            "provider_breakdown": local_summary.provider_breakdown,
            "actions": local_summary.actions,
            "latest_event_at": local_summary.latest_event_at,
        },
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit activity with concise operational risk notes.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "summary": getattr(response, "output_text", ""),
        "metrics": prompt["local_summary"],
    }
