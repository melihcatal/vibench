import os
import boto3
from identity_models import AuditRecord

# Define the DynamoDB table name
AUDIT_TABLE_NAME = os.environ.get("DYNAMODB_AUDIT_TABLE", "FederatedLoginAudit")


def create_audit_table_if_not_exists():
    # AWS DynamoDB client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    # or configured via AWS CLI/SDK default profiles.
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # AWS_REGION is provider-specific
    )

    try:
        table = dynamodb.Table(AUDIT_TABLE_NAME)
        table.load()
        print(f"DynamoDB table '{AUDIT_TABLE_NAME}' already exists.")
        return table
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"DynamoDB table '{AUDIT_TABLE_NAME}' not found. Creating it...")
        table = dynamodb.create_table(
            TableName=AUDIT_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "event_id", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "timestamp", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "event_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",  # On-demand capacity
        )
        table.wait_until_exists()
        print(f"DynamoDB table '{AUDIT_TABLE_NAME}' created successfully.")
        return table
    except Exception as e:
        raise Exception(f"Failed to interact with DynamoDB table: {e}")


def persist_audit_record(record: AuditRecord):
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # AWS_REGION is provider-specific
    )
    table = dynamodb.Table(AUDIT_TABLE_NAME)

    try:
        table.put_item(Item=record.__dict__)
        print(f"Audit record {record.event_id} persisted successfully.")
    except Exception as e:
        raise Exception(f"Failed to persist audit record to DynamoDB: {e}")


if __name__ == "__main__":
    # Ensure the table exists before attempting to write
    try:
        create_audit_table_if_not_exists()

        # Example audit record
        import datetime
        import uuid

        example_record = AuditRecord(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            user_id="user123",
            event_type="LOGIN_SUCCESS",
            details={
                "ip_address": "192.168.1.1",
                "provider": "Google",
                "mfa_used": True,
            },
        )
        persist_audit_record(example_record)

        example_record_2 = AuditRecord(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            user_id="user456",
            event_type="LOGIN_FAILED",
            details={
                "ip_address": "203.0.113.10",
                "provider": "Okta",
                "reason": "Invalid credentials",
            },
        )
        persist_audit_record(example_record_2)

    except Exception as e:
        print(f"Error in main execution: {e}")
