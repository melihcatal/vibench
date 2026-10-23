import datetime
from dataclasses import dataclass
from identity_models import AuditEvent

class AuditSummary:
    """Helper to produce a consolidated summary of federated-login audit events.
    Intended to run after all login events have been persisted.
    """

    @classmethod
    def summarize(cls, events: list[AuditEvent]) -> dict:
        """
        Args:
            events: List of audit records persisted for the login flow.
        Returns:
            A dict containing high-level metrics and a timeline of recent events.
        """
        summary = {
            "total_events": len(events),
            "event_counts": {},
            "recent_events": [],
            "timestamp_range": {},
        }
        if not events:
            return summary
        # Count by event name
        for ev in events:
            summary["event_counts"].setdefault(ev.event_name, 0)
            summary["event_counts"][ev.event_name] += 1
        # Timeline
        timestamps = [cls._parse_iso(ev.payload["timestamp"]) for ev in events]
        summary["timestamp_range"] = {
            "earliest": min(timestamps).isoformat() + "Z",
            "latest": max(timestamps).isoformat() + "Z",
        }
        # Recent events (most recent 5)
        sorted_events = sorted(events, key=lambda e: cls._parse_iso(e.payload["timestamp"]))
        summary["recent_events"] = [
            {"name": e.event_name, "details": e.payload} for e in sorted_events[-5:]
        ]
        return summary

    @staticmethod
    def _parse_iso(ts: str) -> datetime.datetime:
        """Parse ISO 8601 timestamp without timezone info (add UTC).",
        from datetime import datetime
        return datetime.fromisoformat(ts.replace('Z','+00:00'))

    @staticmethod
    def serialize_summary(summary: dict) -> str:
        """Convert summary dict to a pretty‑printed JSON string."""
        import json
        return json.dumps(summary, indent=2)
