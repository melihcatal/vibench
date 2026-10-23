import json
import os
from google.cloud import pubsub_v1
from datetime import datetime


def send_to_dead_letter(message_data, error_reason, dead_letter_topic_id=None):
    """Send failed messages to Google Cloud Pub/Sub dead-letter topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if dead_letter_topic_id is None:
        dead_letter_topic_id = os.environ.get(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
        )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    dead_letter_message = {
        "original_message": message_data,
        "error_reason": error_reason,
        "failed_at": datetime.utcnow().isoformat(),
        "retry_count": message_data.get("retry_count", 0) + 1
        if isinstance(message_data, dict)
        else 0,
    }

    data = json.dumps(dead_letter_message).encode("utf-8")

    future = publisher.publish(
        topic_path, data, error_reason=error_reason, message_type="dead_letter"
    )
    message_id = future.result()

    return {
        "message_id": message_id,
        "dead_letter_topic": topic_path,
        "error_reason": error_reason,
        "provider": "google-cloud-pubsub",
    }


def create_dead_letter_subscription(topic_id, subscription_id):
    """Create a dead-letter subscription for a topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    dead_letter_policy = pubsub_v1.types.DeadLetterPolicy(
        dead_letter_topic=topic_path, max_delivery_attempts=5
    )

    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_path, dead_letter_policy=dead_letter_policy
    )

    created_subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )

    return {
        "subscription_name": created_subscription.name,
        "topic": created_subscription.topic,
        "dead_letter_policy": {
            "dead_letter_topic": created_subscription.dead_letter_policy.dead_letter_topic,
            "max_delivery_attempts": created_subscription.dead_letter_policy.max_delivery_attempts,
        },
        "provider": "google-cloud-pubsub",
    }


if __name__ == "__main__":
    sample_message = {"user_id": "user_456", "action": "purchase", "amount": 100.50}
    result = send_to_dead_letter(sample_message, "Payment processing failed")
    print(f"Sent to dead letter: {result}")
