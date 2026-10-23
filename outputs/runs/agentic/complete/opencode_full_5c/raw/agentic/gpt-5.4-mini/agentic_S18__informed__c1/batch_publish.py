import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, topic_path
from messaging_models import PublishBatchRequest, normalize_payload


def batch_publish(request: PublishBatchRequest):
    publisher = get_publisher()
    topic = topic_path(request.topic)
    futures = []
    for item in request.messages:
        payload = item.get("payload", item)
        attributes = item.get("attributes", {})
        futures.append(
            publisher.publish(topic, data=normalize_payload(payload), **attributes)
        )
    return [future.result() for future in futures]


def main() -> None:
    req = PublishBatchRequest(
        topic="events", messages=[{"payload": {"id": "1"}}, {"payload": {"id": "2"}}]
    )
    print(json.dumps({"message_ids": batch_publish(req)}))


if __name__ == "__main__":
    main()
