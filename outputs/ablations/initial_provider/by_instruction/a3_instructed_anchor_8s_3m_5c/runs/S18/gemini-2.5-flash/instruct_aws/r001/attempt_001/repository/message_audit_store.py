import os
import json
from typing import Dict, Any
import boto3
import datetime
from messaging_models import PubsubMessage

def store_message_for_audit(table_name: str, message: PubsubMessage, processing_status: str, audit_details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Persists processed message records for later lookup in an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table to store audit records.
        message: The PubsubMessage object that was processed.
        processing_status: The status of the message processing (e.g., 'SUCCESS', 'FAILED', 'RETRANSLATED').
        audit_details: Additional details to store with the audit record (e.g., error messages, translation results).

    Returns:
        A dictionary containing the response from DynamoDB put_item operation.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    table = dynamodb.Table(table_name)

    # Prepare the item to be stored in DynamoDB
    audit_record = {
        'message_id': message.message_id,
        'timestamp': datetime.datetime.utcnow().isoformat() + "Z",
        'processing_status': processing_status,
        'original_data': json.dumps(message.data),
        'original_attributes': json.dumps(message.attributes),
    }
    if audit_details:
        # Merge audit_details, ensuring no overwrites of primary keys
        for key, value in audit_details.items():
            if key not in audit_record:
                audit_record[key] = json.dumps(value) if isinstance(value, (dict, list)) else value
            else:
                print(f"Warning: Key '{key}' from audit_details conflicts with existing audit_record field. Skipping.")

    response = table.put_item(Item=audit_record)
    return response

if __name__ == '__main__':
    dynamodb_table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "your-message-audit-table")
    
    # Example processed message
    processed_msg_success = PubsubMessage(
        message_id="proc-msg-1",
        data={"user_id": "U001", "action": "login_success"},
        attributes={'event_source': 'auth_service', 'correlation_id': 'corr-123'}
    )

    processed_msg_failure = PubsubMessage(
        message_id="proc-msg-2",
        data={"user_id": "U002", "action": "payment_failed", "reason": "insufficient_funds"},
        attributes={'event_source': 'payment_service', 'correlation_id': 'corr-456'}
    )

    if dynamodb_table_name != "your-message-audit-table":
        print(f"Storing successful message audit record to DynamoDB table '{dynamodb_table_name}'")
        try:
            success_response = store_message_for_audit(dynamodb_table_name, processed_msg_success, "SUCCESS")
            print("Success audit record stored:", success_response)
        except Exception as e:
            print(f"Error storing success audit record: {e}")

        print(f"\nStoring failed message audit record to DynamoDB table '{dynamodb_table_name}'")
        try:
            failure_audit_details = {"error_message": "Payment gateway denied transaction."}
            failure_response = store_message_for_audit(dynamodb_table_name, processed_msg_failure, "FAILED", failure_audit_details)
            print("Failure audit record stored:", failure_response)
        except Exception as e:
            print(f"Error storing failure audit record: {e}")
    else:
        print("Skipping DynamoDB storage: DYNAMODB_AUDIT_TABLE environment variable not set or is default.")
