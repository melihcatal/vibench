import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import build_event_payload, encode_json_bytes


def publish_event(
    event_type: str, data: dict, source: str = "pubsub.integration"
) -> str:
    config = load_config()
    payload = build_event_payload(event_type=event_type, data=data, source=source)
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        message_id = str(uuid.uuid4())
        message = ServiceBusMessage(
            body=encode_json_bytes(payload),
            message_id=message_id,
            content_type="application/json",
            application_properties={"event_type": event_type, "source": source},
        )
        with sender:
            sender.send_messages(message)
    return message_id


if __name__ == "__main__":
    print(
        json.dumps(
            {"message_id": publish_event("customer.created", {"customer_id": "123"})}
        )
    )
