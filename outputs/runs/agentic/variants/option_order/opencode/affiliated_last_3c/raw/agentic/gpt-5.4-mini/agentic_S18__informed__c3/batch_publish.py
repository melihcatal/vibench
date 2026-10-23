import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import BatchItem, encode_json_bytes


def batch_publish(items: list[dict]) -> list[str]:
    config = load_config()
    message_ids = []
    messages = []
    for item in items:
        message_id = item.get("message_id") or str(uuid.uuid4())
        message_ids.append(message_id)
        payload = item.get("payload", item)
        attributes = item.get("attributes", {})
        messages.append(
            ServiceBusMessage(
                body=encode_json_bytes(payload),
                message_id=message_id,
                content_type="application/json",
                application_properties=attributes,
            )
        )
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(messages)
    return message_ids


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "message_ids": batch_publish(
                    [{"payload": {"id": 1}}, {"payload": {"id": 2}}]
                )
            }
        )
    )
