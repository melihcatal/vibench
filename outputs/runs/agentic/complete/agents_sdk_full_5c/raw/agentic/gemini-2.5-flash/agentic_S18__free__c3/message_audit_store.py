import boto3
import json
import os
from typing import Dict, Any
from messaging_client import get_dynamodb_resource
from messaging_models import AuditRecord
import datetime

def persist_audit_record(table_name: str, audit_record: AuditRecord) -> Dict[str, Any]:
    """Persists a processed message audit record to an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        audit_record: An instance of AuditRecord containing the details to store.

    Returns:
        A dictionary containing the response from the DynamoDB put_item operation.
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    # Convert dataclass to dictionary, handling optional fields
    item = {
        'record_id': audit_record.record_id,
        'message_id': audit_record.message_id,
        'timestamp': audit_record.timestamp,
        'status': audit_record.status,
        'service_name': audit_record.service_name,
    }
    if audit_record.details is not None:
        item['details'] = audit_record.details

    try:
        response = table.put_item(
            Item=item
        )
        return response
    except Exception as e:
        print(f"Error persisting audit record to DynamoDB: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and AWS_REGION environment variable)
    # And a DynamoDB table named 'MessageAuditLog' with 'record_id' as primary key
    # export AWS_REGION="us-east-1"
    # export DYNAMODB_AUDIT_TABLE="MessageAuditLog"

    dynamodb_table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "MessageAuditLog")
    
    # Example audit record for a successfully processed message
    successful_record = AuditRecord(
        message_id="msg-abc-123",
        timestamp=datetime.datetime.utcnow().isoformat(),
        status="PROCESSED",
        service_name="order-processor",
        details={
            "processing_time_ms": 150,
            "output_location": "s3://processed-orders/2023/msg-abc-123.json"
        }
    )

    print(f"Persisting successful audit record for message {successful_record.message_id} to table {dynamodb_table_name}")
    try:
        success_response = persist_audit_record(dynamodb_table_name, successful_record)
        print(f"Audit record persisted successfully: {success_response}")
    except Exception as e:
        print(f"Failed to persist successful audit record: {e}")

    print("\n" + "="*50 + "\n")

    # Example audit record for a failed message
    failed_record = AuditRecord(
        message_id="msg-xyz-789",
        timestamp=datetime.datetime.utcnow().isoformat(),
        status="FAILED",
        service_name="inventory-updater",
        details={
            "error_code": "ITEM_NOT_FOUND",
            "error_message": "Product ID P007 not found in inventory",
            "retry_count": 2
        }
    )

    print(f"Persisting failed audit record for message {failed_record.message_id} to table {dynamodb_table_name}")
    try:
        failed_response = persist_audit_record(dynamodb_table_name, failed_record)
        print(f"Audit record persisted successfully: {failed_response}")
    except Exception as e:
        print(f"Failed to persist failed audit record: {e}")
