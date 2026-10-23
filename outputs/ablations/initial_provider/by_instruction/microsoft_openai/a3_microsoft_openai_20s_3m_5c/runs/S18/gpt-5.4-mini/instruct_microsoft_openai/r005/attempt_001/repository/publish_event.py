import base64
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_config, require
from messaging_models import PublishRequest, PublishResponse, normalize_payload


def publish_event(event, attributes=None):
    config = get_config()
    connection_string = require(config["azure_connection_string"], "AZURE_SERVICE_BUS_CONNECTION_STRING")
    queue_name = require(config["azure_queue_name"], "AZURE_SERVICE_BUS_QUEUE_NAME")
    request = PublishRequest(topic=queue_name, payload=normalize_payload(event), attributes={str(k): str(v) for k, v in (attributes or {}).items()})
    body = json.dumps(request.payload, ensure_ascii=False)
    client = ServiceBusClient.from_connection_string(connection_string)
    with client:
        sender = client.get_queue_sender(queue_name)
        with sender:
            message = ServiceBusMessage(body, application_properties=request.attributes)
            sender.send_messages(message)
            message_id = base64.urlsafe_b64encode(body.encode("utf-8")).decode("ascii")[:32]
            return PublishResponse(provider="azure.servicebus", message_id=message_id, metadata={"queue": queue_name, "attributes": request.attributes}).__dict__


if __name__ == "__main__":
    publish_event({"type": "created", "source": "publish_event"})
