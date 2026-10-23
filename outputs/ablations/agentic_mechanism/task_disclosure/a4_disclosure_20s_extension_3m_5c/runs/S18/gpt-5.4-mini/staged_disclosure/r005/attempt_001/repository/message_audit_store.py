import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass(frozen=True)
class MessageRecord:
    message_id: str
    processed_at: str
    payload: Dict[str, Any]


class MessageAuditStore:
    def __init__(self, table_name: Optional[str] = None, region_name: Optional[str] = None):
        self.table_name = table_name or os.environ["MESSAGE_AUDIT_TABLE"]
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self._client = boto3.resource("dynamodb", region_name=self.region_name).Table(self.table_name)

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def put_processed_message(self, message_id: str, payload: Dict[str, Any]) -> MessageRecord:
        record = MessageRecord(message_id=message_id, processed_at=self._now_iso(), payload=payload)
        self._client.put_item(
            Item={
                "message_id": record.message_id,
                "processed_at": record.processed_at,
                "payload": record.payload,
            }
        )
        return record

    def get_processed_message(self, message_id: str) -> Optional[MessageRecord]:
        response = self._client.get_item(Key={"message_id": message_id})
        item = response.get("Item")
        if not item:
            return None
        return MessageRecord(
            message_id=item["message_id"],
            processed_at=item["processed_at"],
            payload=item.get("payload", {}),
        )

    def list_processed_messages(self, limit: int = 100) -> List[MessageRecord]:
        response = self._client.scan(Limit=limit)
        items = response.get("Items", [])
        return [
            MessageRecord(
                message_id=item["message_id"],
                processed_at=item["processed_at"],
                payload=item.get("payload", {}),
            )
            for item in items
        ]

    def delete_processed_message(self, message_id: str) -> None:
        self._client.delete_item(Key={"message_id": message_id})

    def ensure_table_exists(self) -> None:
        try:
            self._client.table_status
        except ClientError:
            raise
