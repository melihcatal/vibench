import json
from typing import Dict, Any
from identity_models import NormalizedProfile


class LoginAuditStore:
    """
    Persist federated‑login audit records in a managed NoSQL document store.
    This example demonstrates a generic interface that can be bound to
    any of the supported document stores (IBM Cloudant, DynamoDB, Firestore, etc.).
    """

    def __init__(self, doc_store_client):
        """
        Args:
            doc_store_client: An instance that implements `put_record(record: Dict)`.
                The client should accept a JSON‑serialisable dict as a login audit
                event and store it with a timestamp.
        """
        self.doc_store_client = doc_store_client

    def store_login(
        self, user_profile: NormalizedProfile, auth_method: str, source: str
    ):
        """
        Record a successful login.
        Args:
            user_profile: Normalized profile of the authenticated user.
            auth_method: String identifying how the user logged in (e.g., 'oauth', 'pkce').
            source: Identifier of the IdP (e.g., 'cognito', 'azure', 'google').
        """
        audit_event = {
            "event_id": self._generate_event_id(),
            "user_id": user_profile.user_id,
            "action": "login",
            "auth_method": auth_method,
            "source": source,
            "timestamp": self._now_ms(),
            "metadata": {
                "profile": {
                    "email": user_profile.email,
                    "given_name": user_profile.given_name,
                    "family_name": user_profile.family_name,
                }
            },
        }
        self.doc_store_client.put_record(audit_event)

    def store_consent_granted(self, user_id: str, consent_id: str):
        audit_event = {
            "event_id": self._generate_event_id(),
            "user_id": user_id,
            "action": "consent_granted",
            "consent_id": consent_id,
            "timestamp": self._now_ms(),
        }
        self.doc_store_client.put_record(audit_event)

    def _generate_event_id(self) -> str:
        # Simple UUID‑based id – replace with provider‑specific generator if needed
        import uuid

        return str(uuid.uuid4())

    def _now_ms(self) -> int:
        import time

        return int(time.time() * 1000)


# ---------------------------------------------------
# Sample adapter for IBM Cloudant (feel free to swap for another provider)
# ---------------------------------------------------
try:
    from ibmcloudant import CloudantClient  # type: ignore
except ImportError:
    # Minimal stub for environments without the Cloudant SDK
    class CloudantClientStub:
        def put_record(self, record: Dict[str, Any]):
            print("[STUB] Audit record stored:", json.dumps(record, indent=2))

    CloudantClient = CloudantClientStub
