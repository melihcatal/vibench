"""Send failed messages to a Google Cloud Pub/Sub dead-letter destination."""

import json
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import DeadLetterPolicy

from messaging_client import (
    get_pubsub_publisher_client,
    get_pubsub_subscriber_client,
    get_pubsub_config,
)
from messaging_models import ConsumedMessage, DeadLetterRecord


def send_to_dead_letter(
    failed_message: ConsumedMessage,
    dead_letter_topic_id: str,
    original_subscription_id: str,
    failure_reason: str,
    retry_count: int = 0,
) -> DeadLetterRecord:
    """Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        failed_message: The original consumed message that failed processing.
        dead_letter_topic_id: Google Cloud Pub/Sub topic for dead-letter messages.
        original_subscription_id: The subscription the message came from.
        failure_reason: Description of why the message failed.
        retry_count: Number of times the message was retried.

    Returns:
        DeadLetterRecord with tracking information.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    publisher_client = get_pubsub_publisher_client()
    dead_letter_topic_path = publisher_client.topic_path(project_id, dead_letter_topic_id)

    dead_letter_payload = {
        "original_message_id": failed_message.message_id,
        "original_payload": failed_message.payload,
        "original_attributes": failed_message.attributes,
        "original_subscription": original_subscription_id,
        "failure_reason": failure_reason,
        "retry_count": retry_count,
        "dead_letter_timestamp": datetime.now(timezone.utc).isoformat(),
        "dead_letter_id": str(uuid.uuid4()),
    }

    message_body = json.dumps(dead_letter_payload).encode("utf-8")

    attributes = {
        "dead_letter": "true",
        "failure_reason": failure_reason,
        "original_subscription": original_subscription_id,
        "retry_count": str(retry_count),
    }

    future = publisher_client.publish(
        dead_letter_topic_path, data=message_body, **attributes
    )
    dead_letter_message_id = future.result()

    return DeadLetterRecord(
        dead_letter_id=dead_letter_payload["dead_letter_id"],
        original_message_id=failed_message.message_id,
        dead_letter_message_id=dead_letter_message_id,
        dead_letter_topic_path=dead_letter_topic_path,
        failure_reason=failure_reason,
        retry_count=retry_count,
        status="dead_lettered",
    )


def configure_dead_letter_policy(
    subscription_id: str,
    dead_letter_topic_id: str,
    max_delivery_attempts: int = 5,
) -> DeadLetterPolicy:
    """Configure a dead-letter policy on a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: Google Cloud Pub/Sub subscription to configure.
        dead_letter_topic_id: Google Cloud Pub/Sub topic for dead-letter messages.
        max_delivery_attempts: Maximum delivery attempts before dead-lettering.

    Returns:
        Configured DeadLetterPolicy object.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    publisher_client = get_pubsub_publisher_client()
    dead_letter_topic_path = publisher_client.topic_path(project_id, dead_letter_topic_id)

    dead_letter_policy = DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path,
        max_delivery_attempts=max_delivery_attempts,
    )

    return dead_letter_policy
