import os
from messaging_client import FirestoreClient
from messaging_models import AuditRecord
import json

def persist_audit_record(record: AuditRecord):
    client = FirestoreClient()
    doc_ref = client.db.collection("message_audit").document(record.message_id)
    
    # Convert dataclass to dict for Firestore
    record_dict = {
        "timestamp": record.timestamp,
        "status": record.status,
        "payload": record.payload,
        "summary": record.summary,
        "safety_scores": record.safety_scores,
        "translated_payload": record.translated_payload
    }
    
    doc_ref.set(record_dict)
    print(f"Audit record for message ID {record.message_id} persisted to Firestore.")

def get_audit_record(message_id: str) -> AuditRecord:
    client = FirestoreClient()
    doc_ref = client.db.collection("message_audit").document(message_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return AuditRecord(
            message_id=message_id,
            timestamp=data["timestamp"],
            status=data["status"],
            payload=data["payload"],
            summary=data.get("summary"),
            safety_scores=data.get("safety_scores"),
            translated_payload=data.get("translated_payload")
        )
    return None

if __name__ == "__main__":
    # Example usage
    import datetime
    
    sample_audit_record = AuditRecord(
        message_id="audit-test-1",
        timestamp=datetime.datetime.now().isoformat(),
        status="processed",
        payload={"user_id": "user123", "action": "login"},
        summary="User logged in.",
        safety_scores={"TOXICITY": 0.1},
        translated_payload={"action": "connexion"}
    )
    
    try:
        persist_audit_record(sample_audit_record)
        
        retrieved_record = get_audit_record("audit-test-1")
        if retrieved_record:
            print(f"
Retrieved audit record for {retrieved_record.message_id}:")
            print(f"  Status: {retrieved_record.status}")
            print(f"  Payload: {retrieved_record.payload}")
            print(f"  Summary: {retrieved_record.summary}")
            print(f"  Safety Scores: {retrieved_record.safety_scores}")
            print(f"  Translated Payload: {retrieved_record.translated_payload}")
        else:
            print("
Audit record not found.")

    except Exception as e:
        print(f"Error in audit store operations: {e}")
