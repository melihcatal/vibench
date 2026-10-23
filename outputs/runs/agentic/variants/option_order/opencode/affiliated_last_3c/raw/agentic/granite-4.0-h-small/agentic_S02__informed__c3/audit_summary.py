import os
import json
from typing import TypedDict
from identity_models import AuditEvent, AuditEventSeverity


class AuditSummary(TypedDict):
    event_count: int
    critical: int
    high: int
    medium: int
    low: int
    summary_text: str


def audit_summary(events: list[AuditEvent]) -> AuditSummary:
    """Summarize federated-login audit events.
    Calculates total counts per severity and produces a concise textual summary.
    """
    counts = {sev: 0 for sev in AuditEventSeverity}
    for ev in events:
        counts[ev.severity] += 1
    summary = {
        "event_count": len(events),
        "critical": counts["critical"],
        "high": counts["high"],
        "medium": counts["medium"],
        "low": counts["low"],
        "summary_text": (
            f"Federated login audit contains {len(events)} events. "
            f"Critical: {counts['critical']}, High: {counts['high']}, Medium: {counts['medium']}, Low: {counts['low']}"
        ),
    }
    return AuditSummary(**summary)
