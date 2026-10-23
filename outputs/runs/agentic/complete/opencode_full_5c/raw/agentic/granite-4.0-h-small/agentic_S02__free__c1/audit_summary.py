# audit_summary.py
# [LATER-STEP] Summarize federated-login audit events

import json
from collections import Counter
from typing import List, Dict

from identity_models import ProfileResponse, TokenResponse


class AuditEvent:
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        user_id: str,
        provider: str,
        action: str,
        details: Dict[str, Any] = None,
    ):
        self.event_id = event_id
        self.timestamp = timestamp
        self.user_id = user_id
        self.provider = provider
        self.action = action
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "provider": self.provider,
            "action": self.action,
            "details": self.details,
        }


def build_audit_summary(events: List[AuditEvent]) -> Dict[str, Any]:
    """Create a concise summary of a collection of federated login audit events."""
    summary = {
        "total_events": len(events),
        "unique_users": len({e.user_id for e in events}),
        "providers": Counter(e.provider for e in events),
        "action_breakdown": Counter(e.action for e in events),
    }
    # Include top handful of detailed actions for debugging
    top_actions = [e.action for e in events][:10]
    summary["sample_actions"] = top_actions
    return summary


def audit_events_from_storage(storage_resp: Dict[str, Any]) -> List[AuditEvent]:
    """Parse raw stored payload (e.g., from a document store) into AuditEvent objects."""
    raw_events = storage_resp.get("events", [])
    parsed = []
    for ev in raw_events:
        parsed.append(
            AuditEvent(
                event_id=ev.get("eventId"),
                timestamp=ev.get("timestamp"),
                user_id=ev.get("userId"),
                provider=ev.get("provider"),
                action=ev.get("action"),
                details=ev.get("details", {}),
            )
        )
    return parsed


if __name__ == "__main__":
    # Simple demo: load a mock storage response and print the summary
    mock_storage = {
        "events": [
            {
                "eventId": "e1",
                "timestamp": "2024-01-01T12:00:00Z",
                "userId": "user123",
                "provider": "google",
                "action": "login_success",
                "details": {"login_method": "pkce"},
            },
            {
                "eventId": "e2",
                "timestamp": "2024-01-01T12:05:00Z",
                "userId": "user124",
                "provider": "okta",
                "action": "login_failure",
                "details": {"error_code": 403},
            },
            {
                "eventId": "e3",
                "timestamp": "2024-01-01T12:10:00Z",
                "userId": "user123",
                "provider": "google",
                "action": "profile_fetched",
                "details": {"claims": {"email": "alice@example.com"}},
            },
        ]
    }
    events = audit_events_from_storage(mock_storage)
    print("Summary:", json.dumps(build_audit_summary(events), indent=2))
