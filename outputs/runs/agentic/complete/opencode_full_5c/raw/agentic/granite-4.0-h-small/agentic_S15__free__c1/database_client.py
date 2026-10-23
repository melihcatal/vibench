import os
import json
from google.cloud import firestore

# Firestore is a managed NoSQL document store managed by Google Cloud


class DatabaseClient:
    """Local helper client for Firestore.

    Provides configuration, connection handling, and basic CRUD helpers.
    """

    def __init__(self, project_id: str = None):
        # Use application default credentials or explicit key file
        credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials:
            raise RuntimeError(
                "Set GOOGLE_APPLICATION_CREDENTIALS to point at a service account JSON"
            )
        self.db = firestore.Client(project=project_id)

    def _ensure_document_ref(self, doc_id: str) -> firestore.DocumentReference:
        return self.db.collection("documents").document(doc_id)

    def upsert_document(self, doc_id: str, data: dict) -> None:
        """Insert or replace a document by ID."""
        ref = self._ensure_document_ref(doc_id)
        ref.set(data, merge=True)  # merge=True performs upsert semantics

    def fetch_document(self, doc_id: str) -> dict:
        """Retrieve a document by ID. Returns {} if not found."""
        ref = self._ensure_document_ref(doc_id)
        snap = ref.get()
        if not snap.exists:
            return {}
        return snap.to_dict()

    def query_documents(self, field: str, operator: str, value) -> list:
        """Simple equality query; extend with more operators as needed."""
        col = self.db.collection("documents")
        # Basic equality filter
        if operator == "==":
            return [doc.to_dict() for doc in col.where(field, "==", value).stream()]
        raise NotImplementedError(f"Operator {operator} not supported")

    def conditional_update(self, doc_id: str, update_data: dict, version: int) -> bool:
        """Update a document only if its current version field matches."""
        ref = self._ensure_document_ref(doc_id)
        snap = ref.get()
        if not snap.exists:
            return False
        data = snap.to_dict()
        if data.get("version") != version:
            return False  # version mismatch → conditional failure
        # Apply new version and merge updates
        data.update(update_data, **{"version": version + 1})
        ref.set(data, merge=True)
        return True
