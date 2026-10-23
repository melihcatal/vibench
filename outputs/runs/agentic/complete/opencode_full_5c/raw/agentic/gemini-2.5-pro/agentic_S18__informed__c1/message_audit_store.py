import os
import boto3
import uuid
from botocore.exceptions import ClientError
import time


def persist_message_audit(processed_message: dict, table_name: str):
    """
    Persists processed message records for later lookup in Amazon DynamoDB.
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
    except Exception as e:
        print(f"Error connecting to DynamoDB: {e}")
        return None

    audit_id = str(uuid.uuid4())
    timestamp = int(time.time())

    item_to_persist = {
        "auditId": audit_id,
        "receivedTimestamp": timestamp,
        **processed_message,
    }

    try:
        response = table.put_item(Item=item_to_persist)
        print(f"Successfully stored audit record {audit_id} in table {table_name}.")
        return audit_id
    except ClientError as e:
        print(
            f"Error writing to DynamoDB table {table_name}: {e.response['Error']['Message']}"
        )
        return None


if __name__ == "__main__":
    DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_AUDIT_TABLE", "message-audit-log")

    # Example of a processed message record
    processed_message_record = {
        "originalMessageId": "pubsub-message-id-789",
        "status": "PROCESSED_SUCCESSFULLY",
        "summary": "Order #54321 was processed.",
        "safetyCheckPassed": True,
        "sourceLang": "EN",
        "targetLang": "FR",
        "translation": "La commande n°54321 a été traitée.",
    }

    persist_message_audit(processed_message_record, DYNAMODB_TABLE_NAME)
