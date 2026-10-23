import os
import json
from dataclasses import dataclass
from typing import Dict, Any, Optional
from identity_models import LoginRecord

# In a production system this would be a client library for the actual managed store.
# For the demo we persist records in a JSON file on local disk.
DATA_PATH = "/tmp/federated_login_audit.json"


@dataclass
class InMemoryAuditStore:
    records: Dict[str, LoginRecord] = field(default_factory=dict)

    def save(self, record: LoginRecord) -> None:
        self.records[record.user_id] = record
        self._persist()

    def all(self) -> List[LoginRecord]:
        return list(self.records.values())

    def _persist(self) -> None:
        """Dump the in‑memory store to JSON."""
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(list(self.records.values()), f, indent=2)

    @classmethod
    def load(cls) -> "InMemoryAuditStore":
        """Load existing records or create a fresh store."""
        instance = cls()
        if os.path.isfile(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    for r in raw:
                        # Convert back to LoginRecord dataclass
                        lr = LoginRecord(**r)
                        instance.records[lr.user_id] = lr
            except Exception as exc:
                # Corrupt file → start clean
                print(f"Warning: failed to load audit store ({exc}), starting empty.")
        return instance


# ----------------------------------------------------------------------
# PUBLIC API (used by other modules)
# ----------------------------------------------------------------------


def init_audit_store() -> InMemoryAuditStore:
    """Initialise the audit store singleton and return it."""
    return InMemoryAuditStore.load()


# Example test usage
if __name__ == "__main__":
    store = init_audit_store()
    # Simulate a successful login record
    record = LoginRecord(
        user_id="sub12345",
        provider="IBM App ID",
        login_timestamp=int(os.getenv("TEST_TS", "1725000000")),
        auth_method="authorization_code",
        access_token="access-xyz",
        id_token="id-xyz",
        refresh_token="refresh-xyz",
        profile={"email": "user@example.com", "name": "Test User"},
    )
    store.save(record)
    print("Sample record saved. Full audit file contents:")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        print(f.read())
