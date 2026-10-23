import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


class LoginAuditStore:
    def __init__(self, table_name: Optional[str] = None, region_name: Optional[str] = None) -> None:
        self.table_name = table_name or os.environ.get("LOGIN_AUDIT_TABLE") or os.environ.get("DYNAMODB_TABLE_NAME")
        if not self.table_name:
            raise ValueError("Missing audit table name")
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self._client = boto3.resource("dynamodb", region_name=self.region_name).Table(self.table_name)

    def put_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        record = dict(event)
        if "event_id" not in record:
            record["event_id"] = self._default_event_id(record)
        record.setdefault("stored_at", datetime.now(timezone.utc).isoformat())
        self._client.put_item(Item=record)
        return record

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        response = self._client.get_item(Key={"event_id": event_id})
        return response.get("Item")

    @staticmethod
    def _default_event_id(record: Dict[str, Any]) -> str:
        basis = record.get("subject") or record.get("user_id") or record.get("provider") or "login-audit"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        return f"{basis}-{timestamp}"


def create_login_audit_store(table_name: Optional[str] = None, region_name: Optional[str] = None) -> LoginAuditStore:
    return LoginAuditStore(table_name=table_name, region_name=region_name)
