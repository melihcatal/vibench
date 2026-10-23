import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, topic_path
from messaging_models import PublishRequest, normalize_payload


def publish_event(request: PublishRequest) -> str:
    publisher = get_publisher()
    topic = topic_path(request.topic)
    future = publisher.publish(
        topic, data=normalize_payload(request.payload), **request.attributes
    )
    return future.result()


def main() -> None:
    req = PublishRequest(
        topic="events",
        payload={"type": "customer.created"},
        attributes={"source": "pubsub-task"},
    )
    message_id = publish_event(req)
    print(json.dumps({"message_id": message_id}))


if __name__ == "__main__":
    main()
