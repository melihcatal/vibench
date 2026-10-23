import datetime
import json

from messaging_client import get_dynamodb_client
from messaging_models import AuditRecord


def persist_audit_record(record: AuditRecord, config=None):
    config = config or {}
    dynamodb_client = get_dynamodb_client(config.get("region"))
    table_name = config["audit_table_name"]

    try:
        item = {
            "message_id": {"S": record.message_id},
            "timestamp": {"S": record.timestamp},
            "status": {"S": record.status},
            "details": {"S": json.dumps(record.details)}
        }
        dynamodb_client.put_item(TableName=table_name, Item=item)
        return {"status": "success", "message_id": record.message_id}
    except Exception as e:
        return {"status": "failure", "message_id": record.message_id, "error": str(e)}

