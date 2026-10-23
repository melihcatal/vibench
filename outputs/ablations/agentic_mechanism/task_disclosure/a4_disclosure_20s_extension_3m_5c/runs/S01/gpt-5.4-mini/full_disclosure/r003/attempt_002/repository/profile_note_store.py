from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional

from google.cloud import firestore

GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
FIRESTORE_EMULATOR_HOST_ENV = "FIRESTORE_EMULATOR_HOST"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _normalize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def _normalize_mapping(data: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ProfileNoteRecord:
    user_id: str
    note: Optional[str] = None
    support_metadata: Dict[str, Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        object.__setattr__(self, "support_metadata", _normalize_mapping(self.support_metadata))

    def normalized(self) -> "ProfileNoteRecord":
        now = _utcnow().isoformat()
        return ProfileNoteRecord(
            user_id=_normalize_string(self.user_id) or self.user_id,
            note=_normalize_string(self.note),
            support_metadata=self.support_metadata,
            created_at=self.created_at or now,
            updated_at=self.updated_at or now,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ProfileNoteRecord":
        return cls(
            user_id=str(data.get("user_id") or data.get("userId") or ""),
            note=_normalize_string(data.get("note")),
            support_metadata=_normalize_mapping(data.get("support_metadata") or data.get("supportMetadata")),
            created_at=_normalize_string(data.get("created_at") or data.get("createdAt")),
            updated_at=_normalize_string(data.get("updated_at") or data.get("updatedAt")),
        )


@dataclass(frozen=True)
class ProfileNoteWriteResult:
    user_id: str
    path: str
    saved: bool
    record: ProfileNoteRecord

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["record"] = self.record.to_dict()
        return data


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes", client: Optional[firestore.Client] = None):
        self.project_id = project_id or _env(GOOGLE_CLOUD_PROJECT_ENV)
        self.collection_name = collection_name
        self._client = client or firestore.Client(project=self.project_id)

    @property
    def client(self) -> firestore.Client:
        return self._client

    def save(self, record: ProfileNoteRecord) -> ProfileNoteWriteResult:
        normalized = record.normalized()
        doc_ref = self.client.collection(self.collection_name).document(normalized.user_id)
        payload = normalized.to_dict()
        doc_ref.set(payload, merge=True)
        return ProfileNoteWriteResult(user_id=normalized.user_id, path=doc_ref.path, saved=True, record=normalized)

    def load(self, user_id: str) -> Optional[ProfileNoteRecord]:
        doc_ref = self.client.collection(self.collection_name).document(_normalize_string(user_id) or user_id)
        snapshot = doc_ref.get()
        if not snapshot.exists:
            return None
        data = snapshot.to_dict() or {}
        data.setdefault("user_id", doc_ref.id)
        return ProfileNoteRecord.from_dict(data)

    def update_support_metadata(self, user_id: str, support_metadata: Mapping[str, Any]) -> ProfileNoteWriteResult:
        existing = self.load(user_id) or ProfileNoteRecord(user_id=user_id)
        merged = _normalize_mapping(existing.support_metadata)
        merged.update(_normalize_mapping(support_metadata))
        record = ProfileNoteRecord(
            user_id=existing.user_id,
            note=existing.note,
            support_metadata=merged,
            created_at=existing.created_at,
            updated_at=_utcnow().isoformat(),
        )
        return self.save(record)
