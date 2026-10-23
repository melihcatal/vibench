import json
from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, get_topic_name
from messaging_models import PublishResult, normalize_payload, ensure_json_dict


def publish_event(payload, subject: str = "event"):
    body = normalize_payload(payload)
    data = ensure_json_dict(payload)
    client = create_client()
    with client:
        sender = client.get_topic_sender(topic_name=get_topic_name())
        with sender:
            msg = ServiceBusMessage(
                body, content_type="application/json", subject=subject
            )
            msg.application_properties = {
                k: str(v) for k, v in data.items() if k != "body"
            }
            sender.send_messages(msg)
    return PublishResult(
        message_id=data.get("message_id", ""),
        success=True,
        provider="azure-servicebus",
        attributes=data,
    )


def main():
    sample = {"message_id": "event-1", "body": {"status": "created"}}
    result = publish_event(sample)
    print(json.dumps(result.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main()
