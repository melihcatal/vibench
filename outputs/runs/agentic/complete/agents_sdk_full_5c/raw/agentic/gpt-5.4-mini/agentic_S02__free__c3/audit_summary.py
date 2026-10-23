from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping

from identity_models import NormalizedProfile

OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class AuditSummary:
    total_events: int
    by_provider: dict[str, int]
    notable_users: list[str]


def summarize_audit_events(events: Iterable[Mapping[str, object]]) -> AuditSummary:
    provider_counts: Counter[str] = Counter()
    notable_users: list[str] = []
    total = 0
    for event in events:
        total += 1
        provider = str(event.get("provider", "unknown"))
        provider_counts[provider] += 1
        profile = event.get("profile")
        if isinstance(profile, NormalizedProfile) and profile.email:
            notable_users.append(profile.email)
    return AuditSummary(total_events=total, by_provider=dict(provider_counts), notable_users=notable_users)
