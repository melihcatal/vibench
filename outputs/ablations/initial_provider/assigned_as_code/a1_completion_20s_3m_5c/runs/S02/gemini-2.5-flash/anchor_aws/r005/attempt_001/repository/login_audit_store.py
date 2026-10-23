import boto3
import os
import datetime
import json
from identity_models import FederatedLoginAuditRecord

def store_audit_record(record: FederatedLoginAuditRecord, table_name: str):
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    table = dynamodb.Table(table_name)

    try:
        item = {
            "pk": f"USER#{record.user_id}",
            "sk": f"EVENT#{record.timestamp}#{record.event_type}",
            "event_type": record.event_type,
            "user_id": record.user_id,
            "ip_address": record.ip_address,
            "user_agent": record.user_agent,
            "identity_provider": record.identity_provider,
            "status": record.status,
            "details": json.dumps(record.details) # Store details as a JSON string
        }
        table.put_item(Item=item)
    except Exception as e:
        raise RuntimeError(f"Error storing audit record in DynamoDB: {e}")
