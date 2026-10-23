import json


class DatabaseModels:
    """Local request/response helpers for managed NoSQL document store interactions.

    Contains schemas and normalization utilities to adapt between external store
    formats and internal application structures.
    """

    @staticmethod
    def request_to_firestore_payload(payload: dict) -> dict:
        """Normalize arbitrary request fields to Firestore-friendly payload.
        Mostly a no‑op for simple dicts; can be expanded for timestamps, arrays, etc.
        """
        # Firestore can store most native JSON types directly; just ensure no
        # circular references and that values are serializable.
        return payload

    @staticmethod
    def firestore_snapshot_to_response(snap: dict) -> dict:
        """Convert a Firestore document snapshot (or dict) into a normalized response.
        Adds a top‑level 'id' field for consistency.
        """
        if isinstance(snap, dict):
            data = snap
        else:
            data = snap.to_dict() if hasattr(snap, "to_dict") else snap
        return {"id": snap.id if hasattr(snap, "id") else None, **data}
