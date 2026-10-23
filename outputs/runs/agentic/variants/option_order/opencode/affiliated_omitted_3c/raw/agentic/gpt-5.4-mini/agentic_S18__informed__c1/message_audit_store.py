from typing import Any, Dict

import boto3


def persist_message_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("dynamodb")
    table_name = __import__("os").environ.get("DYNAMODB_AUDIT_TABLE", "message_audit")
    item = {k: {"S": str(v)} for k, v in record.items()}
    client.put_item(TableName=table_name, Item=item)
    return {"provider": "amazon-dynamodb", "table": table_name, "stored": True}
