from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from google.cloud import firestore

from identity_client import load_identity_config
from identity_models import normalize_locale


FIRESTORE_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
FIRESTORE_COLLECTION_ENV = "PROFILE_NOTE_COLLECTION"


def _env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _client() -> firestore.Client:
    project = _env(FIRESTORE_PROJECT_ENV) or load_identity_config().client_id
    return firestore.Client(project=project)


def _collection_name() -> str:
    return _env(FIRESTORE_COLLECTION_ENV, "onboarding_profile_notes")


def _normalize_notes(data: Mapping[str, Any]) -> dict[str, Any]:
    user_id = str(data.get("user_id", data.get("userId", ""))).strip()
    if not user_id:
        raise ValueError("user_id is required")
    note = str(data.get("note", data.get("text", data.get("message", "")))).strip()
    if not note:
        raise ValueError("note is required")
    locale = normalize_locale(data.get("locale")) if data.get("locale") is not None else None
    support_tags = data.get("support_tags", data.get("supportTags", [])) or []
    if not isinstance(support_tags, list):
        support_tags = [str(support_tags)]
    metadata = dict(data.get("metadata") or {})
    return {
        "user_id": user_id,
        "note": note,
        "locale": locale,
        "support_tags": [str(tag).strip() for tag in support_tags if str(tag).strip()],
        "metadata": metadata,
    }


@dataclass(frozen=True)
class ProfileNoteRecord:
    ok: bool
    provider: str
    collection: str
    document_id: str
    user_id: str
    note: str
    locale: Optional[str] = None
    support_tags: Optional[list[str]] = None
    metadata: Optional[dict[str, Any]] = None
    created_at: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "provider": self.provider,
            "collection": self.collection,
            "document_id": self.document_id,
            "user_id": self.user_id,
            "note": self.note,
            "locale": self.locale,
            "support_tags": self.support_tags,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


def store_profile_note(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_notes(payload)
    client = _client()
    collection = _collection_name()
    created_at = _utc_now_iso()
    document = client.collection(collection).document()
    record = {
        "provider": "google_firestore",
        "user_id": normalized["user_id"],
        "note": normalized["note"],
        "locale": normalized["locale"],
        "support_tags": normalized["support_tags"],
        "metadata": normalized["metadata"],
        "created_at": created_at,
        "updated_at": created_at,
    }
    document.set(record)
    return ProfileNoteRecord(
        ok=True,
        provider="google_firestore",
        collection=collection,
        document_id=document.id,
        user_id=normalized["user_id"],
        note=normalized["note"],
        locale=normalized["locale"],
        support_tags=normalized["support_tags"],
        metadata=normalized["metadata"],
        created_at=created_at,
    ).as_dict()
