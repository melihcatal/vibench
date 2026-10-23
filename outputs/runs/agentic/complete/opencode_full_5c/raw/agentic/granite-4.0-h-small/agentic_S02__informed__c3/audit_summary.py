import datetime

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS


class AuditEvent:
    def __init__(
        self,
        event_id: str,
        user_id: str,
        timestamp: datetime.datetime,
        event_type: str,
        details: dict,
    ):
        self.event_id = event_id
        self.user_id = user_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.details = details


class AuditSummary:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.event_count = 0
        self.events = []

    def add_event(self, event: AuditEvent):
        self.events.append(event)
        self.event_count += 1

    def summarize(self) -> dict:
        return {
            "user_id": self.user_id,
            "total_events": self.event_count,
            "events": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat(),
                    "event_type": e.event_type,
                    "details": e.details,
                }
                for e in self.events
            ],
        }
