import json
from azure.servicebus import ServiceBusClient

from messaging_client import get_config, require
from messaging_models import MessageRecord, normalize_payload


def consume_event():
    config = get_config()
    client = ServiceBusClient.from_connection_string(require(config["azure_connection_string"], "AZURE_SERVICE_BUS_CONNECTION_STRING"))
    queue_name = require(config["azure_queue_name"], "AZURE_SERVICE_BUS_QUEUE_NAME")
    with client:
        receiver = client.get_queue_receiver(queue_name, max_wait_time=5)
        with receiver:
            for message in receiver:
                payload = normalize_payload(str(message))
                record = MessageRecord(message_id=str(getattr(message, "message_id", "")), payload=payload, attributes={str(k): str(v) for k, v in getattr(message, "application_properties", {}).items()})
                receiver.complete_message(message)
                return record.to_dict()
    return {"message_id": "", "payload": {}, "attributes": {}}


if __name__ == "__main__":
    print(json.dumps(consume_event(), ensure_ascii=False))
