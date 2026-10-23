import json
import os

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import MessagePayload, payload_to_json


def publish_event(event):
    config = load_config()
    payload = MessagePayload(
        message_id=event["message_id"],
        content=event["content"],
        attributes=event.get("attributes", {}),
    )
    with create_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            sender.send_messages(
                ServiceBusMessage(
                    payload_to_json(payload), content_type="application/json"
                )
            )
    return {"published": True, "message_id": payload.message_id}


if __name__ == "__main__":
    body = json.loads(os.environ["EVENT_JSON"])
    print(publish_event(body))
