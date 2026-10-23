from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable

from openai import OpenAI

from identity_models import TokenSet


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    provider: str
    subject: str
    success: bool
    details: str


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    client = OpenAI()
    counts = Counter((event.event_type, event.success) for event in events)
    event_lines = [f"{event.event_type}:{'ok' if event.success else 'fail'}:{event.provider}:{event.subject}" for event in events]
    prompt = "Summarize these federated login audit events concisely:\n" + "\n".join(event_lines) + "\nCounts:" + str(dict(counts))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize security audit logs."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
