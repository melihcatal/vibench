import boto3
import os
from datetime import datetime
from identity_models import AuditRecord


def get_dynamodb_table():
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "federated_login_audit")
    return dynamodb.Table(table_name)


def store_audit_record(record: AuditRecord):
    table = get_dynamodb_table()

    item_data = record.model_dump()
    item_data["timestamp"] = datetime.utcnow().isoformat()

    response = table.put_item(Item=item_data)
    return response


if __name__ == "__main__":
    test_record = AuditRecord(
        event_id="evt_12345",
        user_id="user_abcde",
        event_type="login_success",
        timestamp=datetime.utcnow().isoformat(),
        details={"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"},
    )

    print("Storing audit record...")
    result = store_audit_record(test_record)
    print("DynamoDB response:", result)
