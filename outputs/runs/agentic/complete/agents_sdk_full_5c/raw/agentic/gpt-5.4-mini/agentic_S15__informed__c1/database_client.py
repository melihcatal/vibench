from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import firestore

from database_models import DocumentRecord, normalize_payload


DEFAULT_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "documents")


@lru_cache(maxsize=1)
def get_client() -> firestore.Client:
    return firestore.Client()


@lru_cache(maxsize=1)
def get_collection_name() -> str:
    return DEFAULT_COLLECTION


class FirestoreRepository:
    def __init__(self, client: Optional[firestore.Client] = None, collection_name: Optional[str] = None):
        self.client = client or get_client()
        self.collection_name = collection_name or get_collection_name()

    def _doc_ref(self, document_id: str):
        return self.client.collection(self.collection_name).document(document_id)

    def upsert(self, document_id: str, payload: Dict[str, Any]) -> DocumentRecord:
        clean = normalize_payload(payload)
        self._doc_ref(document_id).set(clean, merge=True)
        return DocumentRecord(id=document_id, data=clean)

    def fetch(self, document_id: str) -> Optional[DocumentRecord]:
        snap = self._doc_ref(document_id).get()
        if not snap.exists:
            return None
        data = dict(snap.to_dict() or {})
        return DocumentRecord(id=snap.id, data=data)

    def query_by_field(self, field_name: str, field_value: Any) -> list[DocumentRecord]:
        docs = self.client.collection(self.collection_name).where(field_name, "==", field_value).stream()
        result: list[DocumentRecord] = []
        for snap in docs:
            result.append(DocumentRecord(id=snap.id, data=dict(snap.to_dict() or {})))
        return result

    def conditional_update(self, document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None) -> Optional[DocumentRecord]:
        ref = self._doc_ref(document_id)
        transaction = self.client.transaction()

        @firestore.transactional
        def _apply(txn):
            snap = ref.get(transaction=txn)
            if not snap.exists:
                return None
            current = dict(snap.to_dict() or {})
            version = int(current.get("version", 0))
            if expected_version is not None and version != expected_version:
                return None
            current.update(normalize_payload(updates))
            current["version"] = version + 1
            txn.set(ref, current, merge=False)
            return DocumentRecord(id=document_id, data=current, version=current["version"])

        return _apply(transaction)
