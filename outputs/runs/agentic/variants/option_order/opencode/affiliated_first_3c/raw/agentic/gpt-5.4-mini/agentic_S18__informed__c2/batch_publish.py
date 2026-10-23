import json
import os

from azure.servicebus import ServiceBusMessage

from messaging_client import build_client, load_config


def batch_publish(events: list[dict]) -> list[str | None]:
    config = load_config()
    with build_client() as client:
        sender = client.get_topic_sender(
            topic_name=config.topic_name or os.environ["AZURE_SERVICE_BUS_TOPIC_NAME"]
        )
        with sender:
            messages = [
                ServiceBusMessage(json.dumps(event), message_id=event.get("id"))
                for event in events
            ]
            sender.send_messages(messages)
            return [message.message_id for message in messages]
