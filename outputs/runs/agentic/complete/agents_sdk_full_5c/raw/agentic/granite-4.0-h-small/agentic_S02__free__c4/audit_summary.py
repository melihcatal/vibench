import json
from datetime import datetime

# Later-step scored file: audit_summary.py
# Summarize federated-login audit events stored in a managed document store (e.g., AWS Timestream, Google Cloud BigQuery)

class AuditEvent:
    def __init__(self, event_id: str, user_id: str, provider: str, event_type: str, timestamp: datetime, details: dict):
        self.event_id = event_id
        self.user_id = user_id
        self.provider = provider
        self.event_type = event_type
        self.timestamp = timestamp
        self.details = details

class AuditSummary:
    def __init__(self):
        self.events_by_type = {}
        self.events_by_provider = {}
        self.total_events = 0

    def add_event(self, event: AuditEvent):
        self.total_events += 1
        self.events_by_type.setdefault(event.event_type, []).append(event)
        self.events_by_provider.setdefault(event.provider, []).append(event)

    def generate_summary(self) -> dict:
        return {
            "total_events": self.total_events,
            "by_type": {t: len(l) for t, l in self.events_by_type.items()},
            "by_provider": {p: len(l) for p, l in self.events_by_provider.items()}
        }

# Example usage with in-memory list of events
def load_audit_events() -> list[AuditEvent]:
    # In real deployment this would be a query to the managed store
    return [
        AuditEvent(
            event_id="e1",
            user_id="u123",
            provider="google",
            event_type="login_success",
            timestamp=datetime.utcnow(),
            details={"ip": "203.0.113.5"}
        ),
        AuditEvent(
            event_id="e2",
            user_id="u124",
            provider="auth0",
            event_type="login_failure",
            timestamp=datetime.utcnow(),
            details={"error_code": "invalid_grant"}
        )
    ]

if __name__ == "__main__":
    events = load_audit_events()
    summary = AuditSummary()
    for ev in events:
        summary.add_event(ev)
    print(json.dumps(summary.generate_summary(), indent=2))
