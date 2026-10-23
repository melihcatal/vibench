from __future__ import annotations

from collections import Counter


def incident_summary(events: list[dict]):
    severities = Counter()
    messages = []
    for event in events:
        message = event.get("message", "")
        messages.append(message)
        severity = event.get("severity") or event.get("level") or "UNKNOWN"
        severities[severity] += 1
    return {"count": len(events), "severities": dict(severities), "sample_messages": messages[:5]}
