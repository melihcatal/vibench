import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import create_servicebus_client, load_config
from messaging_models import PublishRequest, PublishResponse, to_json_text


def publish_event(event_type: str, payload: dict) -> PublishResponse:
    config = load_config()
    request = PublishRequest(event_type=event_type, payload=payload, message_id=str(uuid.uuid4()))
    body = to_json_text({"event_type": request.event_type, "payload": request.payload, "message_id": request.message_id})
    message = ServiceBusMessage(body, message_id=request.message_id, subject=request.event_type, content_type="application/json")
    with create_servicebus_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name) if config.topic_name else client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(message)
    return PublishResponse(message_id=request.message_id, accepted=True)


if __name__ == "__main__":
    print(json.dumps(publish_event("customer.created", {"source": "openai", "status": "new"}).__dict__))
