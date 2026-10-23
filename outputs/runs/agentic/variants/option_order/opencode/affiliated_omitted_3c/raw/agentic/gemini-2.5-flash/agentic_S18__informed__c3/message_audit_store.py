import json
import os
from datetime import datetime
from messaging_client import AWSMessagingClient
from messaging_models import AuditRecord


def persist_audit_record(record: AuditRecord, table_name: str) -> dict:
    """Persists processed message records to Amazon DynamoDB for later lookup."""
    dynamodb_client = AWSMessagingClient().get_dynamodb_client()

    try:
        item = {
            "message_id": {"S": record.message_id},
            "timestamp": {"S": record.timestamp},
            "status": {"S": record.status},
            "payload": {"S": json.dumps(record.payload)},
        }
        if record.processing_details:
            item["processing_details"] = {"S": json.dumps(record.processing_details)}

        response = dynamodb_client.put_item(TableName=table_name, Item=item)
        return {"status": "success", "message": "Audit record persisted successfully."}
    except Exception as e:
        print(f"Error persisting audit record to DynamoDB: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example Usage (replace with actual DynamoDB table name)
    dynamodb_table_name = os.environ.get(
        "AWS_DYNAMODB_AUDIT_TABLE", "MessageAuditRecords"
    )

    sample_audit_record = AuditRecord(
        message_id="msg-abc-123",
        timestamp=datetime.utcnow().isoformat(),
        status="processed",
        payload={
            "event_type": "user_login",
            "user_id": "user-001",
            "ip_address": "192.168.1.1",
        },
        processing_details={"processor_version": "1.0", "duration_ms": 50},
    )

    print(
        f"Attempting to persist audit record to DynamoDB table: {dynamodb_table_name}..."
    )
    result = persist_audit_record(sample_audit_record, dynamodb_table_name)
    print(result)
