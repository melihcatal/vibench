from google.cloud import firestore
from typing import List, Dict, Any
from datetime import datetime, timedelta


class FirestoreAuditStore:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("federated_login_audits")

    def get_audit_events(self, user_id: str, days: int = 7) -> List[Dict[str, Any]]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = self.collection.where("user_id", "==", user_id).where(
            "timestamp", ">=", cutoff.isoformat()
        )
        docs = query.stream()
        return [doc.to_dict() for doc in docs]


def summarize_audit_events(user_id: str) -> dict:
    store = FirestoreAuditStore()
    events = store.get_audit_events(user_id)

    summary = {
        "user_id": user_id,
        "total_events": len(events),
        "event_types": {},
        "timeline": [],
    }

    for event in events:
        event_type = event["event_type"]
        summary["event_types"][event_type] = (
            summary["event_types"].get(event_type, 0) + 1
        )
        summary["timeline"].append(
            {
                "timestamp": event["timestamp"],
                "event_type": event_type,
                "metadata": event["metadata"],
            }
        )

    return summary
