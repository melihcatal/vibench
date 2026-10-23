import json
import os

from azure.servicebus import ServiceBusMessage

from messaging_client import build_client, load_config
from messaging_models import PublishRequest, PublishResponse


def publish_event(event: dict) -> PublishResponse:
    config = load_config()
    request = PublishRequest(body=event)
    with build_client() as client:
        sender = client.get_topic_sender(
            topic_name=config.topic_name or os.environ["AZURE_SERVICE_BUS_TOPIC_NAME"]
        )
        with sender:
            message = ServiceBusMessage(
                json.dumps(request.body), content_type=request.content_type
            )
            sender.send_messages(message)
            return PublishResponse(message_id=getattr(message, "message_id", None))
