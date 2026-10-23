import os
from messaging_client import get_pubsub_publisher_client
from messaging_models import BatchEventMessage, EventMessage
import json


def publish_batch_events(topic_id: str, batch_message: BatchEventMessage) -> List[str]:
    publisher = get_pubsub_publisher_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message in batch_message.messages:
        future = publisher.publish(
            topic_path, message.to_json(), **(message.attributes or {})
        )
        futures.append(future)

    message_ids = [future.result() for future in futures]
    return message_ids


if __name__ == "__main__":
    pass
