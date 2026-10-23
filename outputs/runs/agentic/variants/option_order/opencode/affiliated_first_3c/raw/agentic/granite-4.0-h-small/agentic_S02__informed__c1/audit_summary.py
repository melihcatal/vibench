import json
from typing import List, Dict
from identity_models import NormalizedProfile


class AuditSummaryGenerator:
    """
    Aggregate and summarize federated-login audit events.
    Events are assumed to be stored in a managed NoSQL document store
    (e.g., IBM Cloudant, DynamoDB). This helper demonstrates a possible
    reporting API.
    """

    def __init__(self, store_client):
        """
        Args:
            store_client: An instance that implements get_events() returning
                a list of audit records. The shape of each record is not fixed,
                but for demonstration we expect fields:
                - event_id (str)
                - user_id (str)
                - action (str)   # e.g., 'login', 'consent_granted', 'claim_updated'
                - timestamp (int) # epoch ms
                - meta (Dict)    # free‑form metadata
        """
        self.store_client = store_client

    def build_summary(self, start_ts: int, end_ts: int) -> Dict[str, Any]:
        """
        Produce a concise report covering the period [start_ts, end_ts].
        Example output structure:
            {
                "total_logins": 123,
                "unique_users": 45,
                "top_events": [
                    {"action": "login", "count": 110},
                    {"action": "consent_granted", "count": 8}
                ],
                "recent_users": [
                    {"user_id": "uid123", "last_action": "login", "ts": 1724625600000}
                ],
                # ... any additional aggregates
            }
        """
        events = self.store_client.get_events(start_ts=start_ts, end_ts=end_ts)
        summary: Dict[str, Any] = {
            "total_logins": 0,
            "unique_users": set(),
            "top_events": {},
            "recent_users": [],
        }
        for ev in events:
            if ev["action"] == "login":
                summary["total_logins"] += 1
                summary["unique_users"].add(ev["user_id"])
            summary["top_events"].setdefault(ev["action"], 0)
            summary["top_events"][ev["action"]] += 1
            # Keep the most recent timestamp per user for "recent_users"
            if ev["timestamp"] > (
                summary.get("recent_users_last_seen", {}).get(ev["user_id"], 0)
            ):
                summary["recent_users_last_seen"][ev["user_id"]] = ev["timestamp"]
        summary["unique_users"] = len(summary["unique_users"])
        # Convert recent users set to list of dicts, sorted newest first
        summary["recent_users"] = [
            {
                "user_id": uid,
                "last_action": self._get_latest_action(uid, events),
                "ts": summary["recent_users_last_seen"][uid],
            }
            for uid in summary["recent_users_last_seen"]
        ]
        summary["recent_users"].sort(key=lambda x: x["ts"], reverse=True)
        return summary

    def _get_latest_action(self, user_id: str, events: List[Dict]) -> str:
        """Return the most recent action for a given user_id."""
        user_events = [e for e in events if e["user_id"] == user_id]
        if not user_events:
            return "unknown"
        latest = max(user_events, key=lambda e: e["timestamp"])
        return latest["action"]
