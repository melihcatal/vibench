from __future__ import annotations

from messaging_client import queue_url, sqs_client
from messaging_models import EventMessage


def batch_publish(messages: list[EventMessage]) -> dict[str, list[dict[str, str]]]:
    entries = [
        {
            "Id": message.event_id,
            "MessageBody": message.as_json(),
            "MessageAttributes": {
                key: {"DataType": "String", "StringValue": value}
                for key, value in message.attributes.items()
            },
        }
        for message in messages
    ]
    response = sqs_client().send_message_batch(QueueUrl=queue_url(), Entries=entries)
    return {
        "provider": "aws_sqs",
        "successful": [
            {"id": item["Id"], "message_id": item["MessageId"]}
            for item in response.get("Successful", [])
        ],
        "failed": [
            {
                "id": item["Id"],
                "code": item.get("Code", ""),
                "message": item.get("Message", ""),
            }
            for item in response.get("Failed", [])
        ],
    }
