import os
import json
import boto3
import datetime

def persist_message_record(table_name: str, record_data: dict) -> dict:
    """
    Persists processed message records to an AWS DynamoDB table.
    The record_data should include a primary key (e.g., 'message_id').
    """
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    table = dynamodb.Table(table_name)

    # Add a timestamp if not already present
    if "audited_at" not in record_data:
        record_data["audited_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    try:
        # DynamoDB requires item attributes to not be empty strings or lists/maps
        # Also, needs to handle different types correctly.
        # For simplicity, we'll try to put the item as is, assuming appropriate structure.
        # In a robust application, you'd sanitize/transform data before saving.

        response = table.put_item(
            Item=record_data
        )
        # Check for HTTP status code 200 for success
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return {"status": "success", "message": "Record persisted successfully"}
        else:
            return {"status": "error", "details": f"DynamoDB response: {response}"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION and DYNAMODB_TABLE_NAME environment variables)
    # Ensure AWS credentials are configured
    # table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    # if not table_name:
    #     print("DYNAMODB_TABLE_NAME environment variable not set.")
    # else:
    #     audit_record = {
    #         "message_id": "audit-msg-123",
    #         "event_type": "user_signup",
    #         "processor": "lambda_processor_v1",
    #         "status": "processed",
    #         "payload_summary": {"user_id": "new_user_456", "email_domain": "example.com"}
    #     }
    #     result = persist_message_record(table_name, audit_record)
    #     print(f"Audit record persistence result: {result}")
    pass
