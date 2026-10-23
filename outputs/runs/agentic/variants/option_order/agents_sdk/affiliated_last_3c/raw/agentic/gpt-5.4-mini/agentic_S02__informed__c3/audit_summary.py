from __future__ import annotations

import os
from collections import Counter
from typing import Iterable

from anthropic import Anthropic

from identity_models import AuditEvent


CLIENT = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
MODEL = "claude-3-5-sonnet-20240620"


def audit_summary(events: Iterable[AuditEvent]) -> str:
    counts = Counter(event.event_type for event in events)
    prompt = f"Summarize federated-login audit events for {dict(counts)}. Focus on unusual sign-in patterns and provider issues."
    message = CLIENT.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text if message.content else ""
