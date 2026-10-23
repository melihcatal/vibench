import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ExpenseRecordStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "expense_records"):
        self._client = firestore.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))
        self._collection = self._client.collection(collection_name)

    def normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(record)
        normalized["amount"] = float(normalized["amount"])
        normalized["currency"] = str(normalized.get("currency", "USD")).upper()
        normalized["category"] = str(normalized.get("category", "uncategorized"))
        normalized["merchant"] = str(normalized.get("merchant", ""))
        normalized["occurred_at"] = self._normalize_timestamp(normalized.get("occurred_at"))
        normalized["stored_at"] = datetime.now(timezone.utc).isoformat()
        return normalized

    def save(self, record: Dict[str, Any], record_id: Optional[str] = None) -> str:
        normalized = self.normalize_record(record)
        doc_ref = self._collection.document(record_id) if record_id else self._collection.document()
        doc_ref.set(normalized)
        return doc_ref.id

    def get(self, record_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._collection.document(record_id).get()
        if not snapshot.exists:
            return None
        data = snapshot.to_dict()
        data["id"] = snapshot.id
        return data

    def list(self, limit: int = 100) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for snapshot in self._collection.limit(limit).stream():
            item = snapshot.to_dict()
            item["id"] = snapshot.id
            results.append(item)
        return results

    def delete(self, record_id: str) -> None:
        self._collection.document(record_id).delete()

    def _normalize_timestamp(self, value: Any) -> str:
        if value is None:
            return datetime.now(timezone.utc).isoformat()
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc).isoformat()
        return str(value)
