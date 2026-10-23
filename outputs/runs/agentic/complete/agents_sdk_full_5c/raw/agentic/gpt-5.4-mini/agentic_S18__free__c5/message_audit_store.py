import json
import sys
from typing import Any, Dict

from google.cloud import firestore

from messaging_models import AuditRecord, now_iso


client = firestore.Client()
collection = client.collection("message_audit_records")


def store_audit_record(message: Dict[str, Any]) -> AuditRecord:
    record = AuditRecord(record_id=str(message.get("message_id") or message.get("id") or "unknown"), message_id=str(message.get("message_id") or message.get("id") or "unknown"), stored_at=now_iso(), payload=message)
    collection.document(record.record_id).set({"message_id": record.message_id, "stored_at": record.stored_at, "payload": record.payload, "provider": "google-cloud-firestore"})
    return record


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    record = store_audit_record(message)
    print(json.dumps({"record_id": record.record_id, "message_id": record.message_id, "stored_at": record.stored_at}, ensure_ascii=False))
