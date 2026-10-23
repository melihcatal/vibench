from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

import boto3

from messaging_models import BatchPublishItem, MessageEvent


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def sqs_client():
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    return boto3.client("sqs", region_name=region_name)


def get_queue_url(name_env_var: str) -> str:
    return get_env(name_env_var)


def serialize_attributes(attributes: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    return {
        key: {"DataType": "String", "StringValue": str(value)}
        for key, value in attributes.items()
    }


def event_to_sqs_message(event: MessageEvent) -> Dict[str, Any]:
    return {
        "MessageBody": json.dumps(
            event.to_dict(), separators=(",", ":"), ensure_ascii=False
        ),
        "MessageAttributes": serialize_attributes(event.attributes),
    }


def batch_entries(items: Iterable[BatchPublishItem]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for item in items:
        message = event_to_sqs_message(item.event)
        entries.append(
            {
                "Id": item.entry_id,
                "MessageBody": message["MessageBody"],
                "MessageAttributes": message["MessageAttributes"],
            }
        )
    return entries
