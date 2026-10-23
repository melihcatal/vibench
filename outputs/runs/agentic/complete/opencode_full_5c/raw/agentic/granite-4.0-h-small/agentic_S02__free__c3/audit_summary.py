# audit_summary.py
# LATER-STEP: Summarizes federated-login audit events stored in the managed document store

import json
from datetime import datetime
from typing import List, Dict, Any


# Simulated document store client (replace with actual managed store SDK)
class DocumentStore:
    def __init__(self):
        # In‑memory storage for demo; real implementation would connect to e.g., DynamoDB, Firestore, etc.
        self._store = []

    def append(self, event: Dict[str, Any]) -> None:
        self._store.append(event)

    def all(self) -> List[Dict[str, Any]]:
        return list(self._store)


doc_store = DocumentStore()

# Accepted event keys (example schema for federated login)
# Each event should contain at least: event_id, user_id, timestamp, type, details
EVENT_TYPE_LOGIN_SUCCESS = "login_success"
EVENT_TYPE_CODE_EXCHANGE = "code_exchange"
EVENT_TYPE_CLAIM_MODERATION = "claim_moderation"
EVENT_TYPE_CONSENT_CAPTURE = "consent_capture"


def summarize_last_n_events(n: int = 10) -> str:
    """Generate a human‑readable summary of the N most recent audit events."""
    events = doc_store.all()
    recent = events[-n:] if len(events) >= n else events
    lines = []
    for ev in recent:
        t = datetime.fromisoformat(ev["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(
            f"[{t}] {ev['type']} – User {ev['user_id']} – {ev.get('details', '')}"
        )
    return "\n".join(lines)


# Helper to add audit records (used by other modules)
# In production these would be async async writes to the managed store


def record_event(event_type: str, user_id: str, details: Dict[str, Any] = None) -> None:
    record = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": event_type,
        "details": details or {},
    }
    doc_store.append(record)


# Example usage for testing
if __name__ == "__main__":
    # Clear the demo store
    doc_store._store = []
    # Record a handful of demo events
    record_event(
        EVENT_TYPE_LOGIN_SUCCESS, user_id="u123", details={"ip": "203.0.113.5"}
    )
    record_event(
        EVENT_TYPE_CODE_EXCHANGE, user_id="u123", details={"access_token": "tok_abc"}
    )
    record_event(
        EVENT_TYPE_CLAIM_MODERATION,
        user_id="u123",
        details={"claim": "email", "status": "approved"},
    )
    record_event(
        EVENT_TYPE_CONSENT_CAPTURE,
        user_id="u123",
        details={"consent_text": "I agree to ..."},
    )
    print("Audit summary:")
    print(summarize_last_n_events(4))
