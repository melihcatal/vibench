import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import create_servicebus_client, load_config
from messaging_models import normalize_records, to_json_text


def publish_batch(records: list[dict]) -> dict:
    config = load_config()
    normalized = normalize_records(records)
    messages = []
    ids = []
    for record in normalized:
        message_id = record.get("message_id") or str(uuid.uuid4())
        ids.append(message_id)
        messages.append(ServiceBusMessage(to_json_text(record), message_id=message_id, application_properties={"record_type": record.get("type", "event")}, content_type="application/json"))
    with create_servicebus_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name) if config.topic_name else client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(messages)
    return {"accepted": True, "count": len(messages), "message_ids": ids}


if __name__ == "__main__":
    print(json.dumps(publish_batch([{"id": "1", "type": "batch"}, {"id": "2", "type": "batch"}])))
