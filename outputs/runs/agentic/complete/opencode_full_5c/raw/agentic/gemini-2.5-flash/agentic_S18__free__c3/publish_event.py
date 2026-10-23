import json
from concurrent import futures
from messaging_client import get_publisher_client, PUBLISH_TOPIC_ID
from messaging_models import PubsubMessage, PublishResponse


def publish_json_event(message: PubsubMessage) -> PublishResponse:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(publisher.project, PUBLISH_TOPIC_ID)

    data = json.dumps(message.data).encode("utf-8")

    future = publisher.publish(topic_path, data, **message.attributes)
    message_id = future.result()  # Blocks until the message is published

    return PublishResponse(message_id=message_id)
