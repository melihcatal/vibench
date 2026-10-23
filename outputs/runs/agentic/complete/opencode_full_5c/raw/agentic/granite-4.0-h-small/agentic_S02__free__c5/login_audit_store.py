from datetime import datetime
from typing import Any, Dict, List


class LoginAuditStore:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def persist(self, record: Dict[str, Any]) -> None:
        """Store a single audit record."""
        record["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.records.append(record)

    def get_all(self) -> List[Dict[str, Any]]:
        return self.records

    def summarize(self) -> str:
        return "\\n".join(
            [
                f"{r['action']} - {r['principal']} - {r['timestamp']}"
                for r in self.records
            ]
        )


# In-memory example usage (remove in real service)
if __name__ == "__main__":
    store = LoginAuditStore()
    store.persist(
        {"action": "login", "principal": "user1", "summary": "Successful OAuth login"}
    )
    store.persist(
        {"action": "consent", "principal": "user1", "summary": "Consent granted"}
    )
    print("Audit Summary:")
    print(store.summarize())
