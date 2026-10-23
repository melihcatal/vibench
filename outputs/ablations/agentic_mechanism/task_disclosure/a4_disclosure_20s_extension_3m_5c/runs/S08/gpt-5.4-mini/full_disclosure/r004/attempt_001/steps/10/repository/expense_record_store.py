import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Optional

try:
    from google.cloud import firestore
except Exception as exc:  # pragma: no cover
    firestore = None
    _firestore_import_error = exc
else:
    _firestore_import_error = None


class ExpenseRecordStoreError(RuntimeError):
    pass


class ExpenseRecordStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.collection_name = collection_name or os.getenv("EXPENSE_RECORD_COLLECTION", "expense_records")
        if firestore is None:
            raise ExpenseRecordStoreError(f"google-cloud-firestore is required: {_firestore_import_error}")
        self.client = firestore.Client(project=self.project_id)
        self.collection = self.client.collection(self.collection_name)

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: ExpenseRecordStore._normalize_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [ExpenseRecordStore._normalize_value(v) for v in value]
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc).isoformat()
        return value

    def _record_id(self, record: Dict[str, Any]) -> str:
        for key in ("expense_id", "record_id", "document_id", "id"):
            value = record.get(key)
            if value:
                return str(value)
        vendor = str(record.get("vendor", "unknown")).strip().lower().replace(" ", "_")
        date = str(record.get("date", datetime.now(timezone.utc).date().isoformat()))
        total = str(record.get("total", "0"))
        return f"{vendor}_{date}_{total}".replace("/", "-")

    def save(self, normalized_record: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(normalized_record, dict):
            raise ExpenseRecordStoreError("normalized_record must be a dictionary")
        record = self._normalize_value(normalized_record)
        record_id = self._record_id(record)
        payload = {
            **record,
            "provider": "google-cloud-firestore",
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
        self.collection.document(record_id).set(payload)
        return {"record_id": record_id, "collection": self.collection_name, "provider": "google-cloud-firestore"}

    def save_many(self, normalized_records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for record in normalized_records:
            results.append(self.save(record))
        return results


def save_expense_record(normalized_record: Dict[str, Any], project_id: Optional[str] = None, collection_name: Optional[str] = None) -> Dict[str, Any]:
    return ExpenseRecordStore(project_id=project_id, collection_name=collection_name).save(normalized_record)
