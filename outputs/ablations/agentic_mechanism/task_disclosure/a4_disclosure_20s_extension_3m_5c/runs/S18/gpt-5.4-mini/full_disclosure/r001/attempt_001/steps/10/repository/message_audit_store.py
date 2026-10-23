import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


class MessageAuditStore:
    def __init__(self, table_name: Optional[str] = None, region_name: Optional[str] = None):
        self.table_name = table_name or os.environ.get("DYNAMODB_AUDIT_TABLE")
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        if not self.table_name:
            raise ValueError("DYNAMODB_AUDIT_TABLE is required")
        self._resource = boto3.resource("dynamodb", region_name=self.region_name)
        self._table = self._resource.Table(self.table_name)

    @staticmethod
    def _utc_now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _normalize_record(message_id: str, payload: Dict[str, Any], status: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        record = {
            "message_id": message_id,
            "status": status,
            "payload": payload,
            "processed_at": MessageAuditStore._utc_now_iso(),
        }
        if metadata:
            record["metadata"] = metadata
        return record

    def put_record(self, message_id: str, payload: Dict[str, Any], status: str = "processed", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        record = self._normalize_record(message_id, payload, status, metadata)
        self._table.put_item(Item=record)
        return record

    def get_record(self, message_id: str) -> Optional[Dict[str, Any]]:
        response = self._table.get_item(Key={"message_id": message_id})
        return response.get("Item")

    def delete_record(self, message_id: str) -> bool:
        try:
            self._table.delete_item(Key={"message_id": message_id})
            return True
        except ClientError:
            return False

    def record_processed_message(self, message_id: str, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.put_record(message_id=message_id, payload=payload, status="processed", metadata=metadata)
