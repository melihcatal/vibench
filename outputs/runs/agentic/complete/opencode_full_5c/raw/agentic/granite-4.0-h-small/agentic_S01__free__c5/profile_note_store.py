import os
import json
import requests
from identity_client import IdentityClient
from identity_models import NotePayload, NoteResult

# Provider: Managed document store SaaS (e.g., DocumentDB Cloud)
BASE_URL = os.getenv("DOCUMENT_STORE_URL", "https://api.documentdb.example.com")
API_KEY = os.getenv("DOCUMENT_STORE_API_KEY")


class NoteClient(IdentityClient):
    """Wrapper for document store CRUD operations."""

    pass  # reuse generic http methods


def store_onboarding_note(user_id: str, notes: dict) -> NoteResult:
    """Persist onboarding notes and support metadata in the managed document store.
    Returns a NoteResult confirming storage or raising an exception.
    """
    payload = NotePayload(user_id=user_id, notes=notes).to_dict()
    client = NoteClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/notes", json=payload)
    if response.status_code != 201:
        raise RuntimeError(f"Note storage error: {response.text}")
    return NoteResult.from_dict(response.json())


# ---------------------------------------------------------------------------
# DTOs for the document store provider
# ---------------------------------------------------------------------------
class NotePayload:
    def __init__(self, user_id: str, notes: dict):
        self.user_id = user_id
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "notes": self.notes,
        }


class NoteResult:
    def __init__(self, document_id: str):
        self.document_id = document_id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NoteResult:
        return cls(document_id=data.get("id") or data.get("document_id"))
