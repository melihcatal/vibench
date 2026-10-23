import os
from typing import Dict, Any, List, Optional
from google.cloud import firestore
from datetime import datetime
import json


class MessageAuditStore:
    """Persist processed message records to Google Cloud Firestore for later lookup."""

    def __init__(self, collection_name: str = "message_audit"):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
        self.collection_name = collection_name
        self.db = None

    def get_client(self) -> firestore.Client:
        """Get or create Firestore client."""
        if self.db is None:
            self.db = firestore.Client(project=self.project_id)
        return self.db

    def store_message_record(
        self, message_data: Dict[str, Any], processing_result: Dict[str, Any]
    ) -> str:
        """Store a processed message record in Firestore."""
        db = self.get_client()

        record_id = message_data.get(
            "message_id", f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        )

        audit_record = {
            "message_id": record_id,
            "original_data": message_data,
            "processing_result": processing_result,
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "status": processing_result.get("status", "unknown"),
            "message_type": message_data.get("event_type", "unknown"),
        }

        doc_ref = db.collection(self.collection_name).document(record_id)
        doc_ref.set(audit_record)

        return record_id

    def batch_store_records(self, records: List[Dict[str, Any]]) -> List[str]:
        """Store multiple message records in a batch."""
        db = self.get_client()
        batch = db.batch()
        record_ids = []

        for record in records:
            message_data = record.get("message_data", {})
            processing_result = record.get("processing_result", {})

            record_id = message_data.get(
                "message_id", f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
            )

            audit_record = {
                "message_id": record_id,
                "original_data": message_data,
                "processing_result": processing_result,
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "status": processing_result.get("status", "unknown"),
                "message_type": message_data.get("event_type", "unknown"),
            }

            doc_ref = db.collection(self.collection_name).document(record_id)
            batch.set(doc_ref, audit_record)
            record_ids.append(record_id)

        batch.commit()
        return record_ids

    def get_message_record(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a message record from Firestore by ID."""
        db = self.get_client()
        doc_ref = db.collection(self.collection_name).document(message_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        return None

    def query_records(
        self, filters: Dict[str, Any], limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Query message records with filters."""
        db = self.get_client()
        query = db.collection(self.collection_name)

        for field, value in filters.items():
            query = query.where(field, "==", value)

        query = query.limit(limit)
        results = query.stream()

        return [doc.to_dict() for doc in results]

    def get_processing_stats(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Get processing statistics for the given time range."""
        db = self.get_client()

        cutoff_time = datetime.utcnow().timestamp() - (time_range_hours * 3600)
        cutoff_date = datetime.fromtimestamp(cutoff_time)

        query = db.collection(self.collection_name).where(
            "processed_at", ">=", cutoff_date.isoformat() + "Z"
        )

        total = 0
        by_status = {}
        by_type = {}

        for doc in query.stream():
            data = doc.to_dict()
            total += 1

            status = data.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1

            msg_type = data.get("message_type", "unknown")
            by_type[msg_type] = by_type.get(msg_type, 0) + 1

        return {
            "total_messages": total,
            "by_status": by_status,
            "by_type": by_type,
            "time_range_hours": time_range_hours,
        }


if __name__ == "__main__":
    audit_store = MessageAuditStore()

    sample_message = {
        "message_id": "msg_12345",
        "event_type": "order_created",
        "customer_id": "cust_12345",
        "amount": 99.99,
        "timestamp": "2024-01-15T10:30:00Z",
    }

    sample_result = {
        "status": "success",
        "processing_time": 0.5,
        "processed_by": "order_service",
        "notes": "Order created successfully",
    }

    try:
        record_id = audit_store.store_message_record(sample_message, sample_result)
        print(f"Stored message record with ID: {record_id}")

        retrieved = audit_store.get_message_record(record_id)
        if retrieved:
            print(f"Retrieved record: {json.dumps(retrieved, indent=2)}")
    except Exception as e:
        print(f"Failed to store/retrieve message record: {e}")
