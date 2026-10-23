import os
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubsubMessage, PublishResponse


def dead_letter(
    dead_letter_topic_id: str, failed_message: PubsubMessage
) -> PublishResponse:
    """Sends failed messages to a dead-letter destination (Pub/Sub topic)."""
    client = PubSubClient()
    dead_letter_topic_path = client.get_topic_path(dead_letter_topic_id)

    # Add an attribute to indicate it's a dead-letter message, if not already present
    attributes = failed_message.attributes or {}
    attributes["dead_letter_reason"] = attributes.get(
        "dead_letter_reason", "unprocessed_message"
    )

    future = client.publisher.publish(
        dead_letter_topic_path, failed_message.to_json().encode("utf-8"), **attributes
    )
    message_id = future.result()
    return PublishResponse(message_ids=[message_id])
