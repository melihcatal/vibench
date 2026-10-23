from __future__ import annotations

import json
from typing import Any

from messaging_client import publish_batch_to_sqs


def batch_publish(messages: list[dict[str, Any]]) -> dict[str, Any]:
    entries = []
    for item in messages:
        message_id = str(item["id"])
        body = json.dumps(item["payload"], ensure_ascii=False)
        attributes = {
            key: {"DataType": "String", "StringValue": str(value)}
            for key, value in item.get("attributes", {}).items()
        }
        entries.append(
            {"Id": message_id, "MessageBody": body, "MessageAttributes": attributes}
        )
    response = publish_batch_to_sqs(entries)
    return {
        "successful": response.get("Successful", []),
        "failed": response.get("Failed", []),
    }
