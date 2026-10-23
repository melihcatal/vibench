from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from messaging_models import MessageAuditRecord


@dataclass
class Summary:
    total: int
    statuses: dict[str, int]
    generated_at: str


def summarize_messages(records: Iterable[MessageAuditRecord]) -> Summary:
    counts = Counter(record.status for record in records)
    total = sum(counts.values())
    return Summary(total=total, statuses=dict(counts), generated_at=datetime.now(timezone.utc).isoformat())
