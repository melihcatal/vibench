import json
from datetime import datetime

# Simulated managed document store client (e.g., Azure Cosmos DB, AWS DocumentDB)

class ManagedStore:
    def __init__(self, database, collection):
        self.database = database
        self.collection = collection
        # In production initialize a proper client SDK here
    
    def save_audit(self, record: dict):
        # Placeholder: just append to an in‑memory list
        if not hasattr(self, "_audit_logs"):
            self._audit_logs = []
        self._audit_logs.append(record)
    
    def query_by_user(self, user_id: str):
        # Return all records for the user
        return [r for r in getattr(self, "_audit_logs", []) if r.get("user_id") == user_id]
    
    def count_today(self):
        today = datetime.utcnow().date()
        return sum(1 for r in getattr(self, "_audit_logs", []) if r.get("timestamp").date() == today)

# Audit summary producer
def summarize_audit(user_id: str, store: ManagedStore):
    events = store.query_by_user(user_id)
    if not events:
        return {"user_id": user_id, "login_events": 0, "auth_methods": [], "last_login": None}
    login_events = [e for e in events if e["event"] == "login"]
    auth_methods = sorted({e["auth_method"] for e in login_events})
    last_login = max(login_events, key=lambda e: e["timestamp"]).get("timestamp")
    return {
        "user_id": user_id,
        "login_events": len(login_events),
        "auth_methods": auth_methods,
        "last_login": last_login.isoformat() if last_login else None
    }

# Example usage (requires a real store init)
if __name__ == "__main__":
    pass
