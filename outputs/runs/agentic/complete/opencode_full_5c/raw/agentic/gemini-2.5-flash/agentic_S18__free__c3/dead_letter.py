import json
from concurrent import futures
from messaging_client import get_publisher_client, DEAD_LETTER_TOPIC_ID
from messaging_models import PubsubMessage, PublishResponse


def send_to_dead_letter(message: PubsubMessage) -> PublishResponse:
    """Sends a failed message to a Google Cloud Pub/Sub dead-letter topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(publisher.project, DEAD_LETTER_TOPIC_ID)

    data = json.dumps(message.data).encode("utf-8")

    future = publisher.publish(topic_path, data, **message.attributes)
    message_id = future.result()

    return PublishResponse(message_id=message_id)
