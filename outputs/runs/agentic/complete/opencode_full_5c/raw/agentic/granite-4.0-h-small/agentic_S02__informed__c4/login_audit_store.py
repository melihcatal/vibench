import os
import json
from typing import Dict
from identity_models import AuditEvent

# Simulated managed NoSQL document store client (placeholder for later integration)

class ManagedDocumentStoreClient:
    """Placeholder client that writes audit events to a local JSON file.
    In production this would be replaced with a real SDK (e.g., pymongo, boto3, etc.).
    """

    def __init__(self):
        self.path = os.getenv("FEDERATED_LOGIN_AUDIT_FILE", "/tmp/federated_audit.jsonl")

    def store_event(self, event: AuditEvent) -> None:
        """Append a single audit event as a JSON line."""
        try:
            with open(self.path, "a") as f:
                f.write(json.dumps(event) + "\\n")
        except Exception as e:
            # In a real system you might raise or log here
            print("Failed to store audit event:", e)

# Singleton instance for the module
store_client = ManagedDocumentStoreClient()


def store_federated_login_audit(event: AuditEvent):
    """Public helper to persist a federated‑login audit record."
    store_client.store_event(event)

if __name__ == "__main__":
    # Example audit event
    sample = {
        "event_type": "login_success",
        "user_id": "sub123",
        "timestamp": int(os.time()),
        "details": {
            "provider": "Alibaba IDaaS",
            "access_token": "token-abc",
            "claims": {
                "sub": "sub123",
                "name": "Alice"
            }
        }
    }
    store_federated_login_audit(sample)
    print("Audit stored at", sample["details"]["provider"])