from __future__ import annotations

from dataclasses import dataclass
from typing import List

from query_error_logs import query_error_logs


def incident_summary(hours: int = 12) -> str:
    result = query_error_logs(hours=hours)
    messages: List[str] = result.messages()
    count = len(messages)
    top = messages[:5]
    return f"Datadog incident review: {count} error logs in the last {hours}h. Sample: {'; '.join(top)}"
