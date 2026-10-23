from __future__ import annotations

import json
from typing import Iterable, List, Optional

from openai import OpenAI

from identity_models import AuditRecord, AuditSummary


class FederatedLoginAuditSummarizer:
    def __init__(self, client: Optional[OpenAI] = None, model: str = "gpt-4o-mini"):
        self.client = client or OpenAI()
        self.model = model

    def summarize(self, events: Iterable[AuditRecord]) -> AuditSummary:
        event_list: List[AuditRecord] = list(events)
        success = sum(1 for event in event_list if event.event_type == "login_success")
        failures = sum(1 for event in event_list if event.event_type == "login_failure")
        subjects = {event.subject for event in event_list if event.subject}
        payload = [
            {
                "event_type": event.event_type,
                "subject": event.subject,
                "provider": event.provider,
                "timestamp": event.timestamp,
                "details": event.details,
            }
            for event in event_list
        ]
        completion = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Summarize federated login audit activity with security-relevant patterns and concise findings.",
                },
                {
                    "role": "user",
                    "content": json.dumps(payload),
                },
            ],
        )
        summary_text = completion.output_text
        provider = event_list[0].provider if event_list else "Auth0 Authentication API"
        return AuditSummary(
            total_events=len(event_list),
            successful_logins=success,
            failed_logins=failures,
            unique_subjects=len(subjects),
            provider=provider,
            model=self.model,
            summary_text=summary_text,
        )
