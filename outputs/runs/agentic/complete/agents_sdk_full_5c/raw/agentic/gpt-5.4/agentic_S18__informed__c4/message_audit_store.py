from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from messaging_client import get_dynamodb_resource


TABLE_NAME = os.getenv("DYNAMODB_AUDIT_TABLE", "message-audit-records")
PROVIDER = "amazon_dynamodb"


def persist_message_record(record: Dict[str, Any], table_name: str = TABLE_NAME) -> Dict[str, Any]:
    if "message_id" not in record:
        raise ValueError("record must include message_id")
    resource = get_dynamodb_resource()
    table = resource.Table(table_name)
    item = {
        **record,
        "provider": PROVIDER,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return {
        "provider": PROVIDER,
        "table_name": table_name,
        "message_id": item["message_id"],
        "status": "stored",
    }
