from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

DYNAMODB_TABLE_NAME_ENV = "PROFILE_NOTE_STORE_TABLE"
AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not metadata:
        return {}
    normalized: Dict[str, Any] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            normalized[str(key)] = value
        else:
            normalized[str(key)] = json.loads(json.dumps(value, default=str))
    return normalized


@dataclass
class ProfileNoteRecord:
    account_id: str
    note_id: str
    note: str
    support_metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_item(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "note_id": self.note_id,
            "note": self.note,
            "support_metadata": _normalize_metadata(self.support_metadata),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ProfileNoteStore:
    def __init__(self, table_name: Optional[str] = None, region_name: Optional[str] = None) -> None:
        self.table_name = table_name or os.environ.get(DYNAMODB_TABLE_NAME_ENV)
        if not self.table_name:
            raise ValueError("PROFILE_NOTE_STORE_TABLE is required")
        self.region_name = (
            region_name
            or os.environ.get(AWS_REGION_ENV)
            or os.environ.get(AWS_DEFAULT_REGION_ENV)
        )
        self._resource = boto3.resource("dynamodb", region_name=self.region_name)
        self._table = self._resource.Table(self.table_name)

    def save_note(
        self,
        account_id: str,
        note: str,
        note_id: Optional[str] = None,
        support_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not account_id:
            raise ValueError("account_id is required")
        if not note:
            raise ValueError("note is required")
        record = ProfileNoteRecord(
            account_id=account_id,
            note_id=note_id or self._generate_note_id(account_id, note),
            note=note,
            support_metadata=support_metadata or {},
        )
        item = record.to_item()
        self._table.put_item(Item=item)
        return item

    def get_note(self, account_id: str, note_id: str) -> Dict[str, Any]:
        if not account_id or not note_id:
            raise ValueError("account_id and note_id are required")
        response = self._table.get_item(Key={"account_id": account_id, "note_id": note_id})
        item = response.get("Item")
        if not item:
            raise KeyError(f"note not found: {account_id}/{note_id}")
        return item

    def list_notes(self, account_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        if not account_id:
            raise ValueError("account_id is required")
        response = self._table.query(
            KeyConditionExpression="account_id = :account_id",
            ExpressionAttributeValues={":account_id": account_id},
            Limit=limit,
            ScanIndexForward=False,
        )
        return response.get("Items", [])

    def update_support_metadata(
        self,
        account_id: str,
        note_id: str,
        support_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not account_id or not note_id:
            raise ValueError("account_id and note_id are required")
        normalized = _normalize_metadata(support_metadata)
        if not normalized:
            return self.get_note(account_id, note_id)
        updated_at = _utc_now_iso()
        update_expression = "SET support_metadata = :support_metadata, updated_at = :updated_at"
        response = self._table.update_item(
            Key={"account_id": account_id, "note_id": note_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues={
                ":support_metadata": normalized,
                ":updated_at": updated_at,
            },
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes", {})

    def delete_note(self, account_id: str, note_id: str) -> None:
        if not account_id or not note_id:
            raise ValueError("account_id and note_id are required")
        self._table.delete_item(Key={"account_id": account_id, "note_id": note_id})

    def _generate_note_id(self, account_id: str, note: str) -> str:
        seed = f"{account_id}:{note}:{_utc_now_iso()}"
        return str(abs(hash(seed)))


def get_profile_note_store(table_name: Optional[str] = None, region_name: Optional[str] = None) -> ProfileNoteStore:
    return ProfileNoteStore(table_name=table_name, region_name=region_name)
