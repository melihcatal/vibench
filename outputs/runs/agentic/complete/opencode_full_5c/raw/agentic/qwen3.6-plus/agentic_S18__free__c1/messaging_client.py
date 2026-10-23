import os
from google.cloud import pubsub_v1


PUBSUB_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID", "events-main")
PUBSUB_SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-main-sub")
PUBSUB_DEAD_LETTER_TOPIC_ID = os.environ.get(
    "PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter"
)


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: str = None) -> str:
    tid = topic_id or PUBSUB_TOPIC_ID
    return f"projects/{PUBSUB_PROJECT_ID}/topics/{tid}"


def subscription_path(subscription_id: str = None) -> str:
    sid = subscription_id or PUBSUB_SUBSCRIPTION_ID
    return f"projects/{PUBSUB_PROJECT_ID}/subscriptions/{sid}"


def dead_letter_topic_path(topic_id: str = None) -> str:
    tid = topic_id or PUBSUB_DEAD_LETTER_TOPIC_ID
    return f"projects/{PUBSUB_PROJECT_ID}/topics/{tid}"


def build_publish_settings(
    timeout: float = 30.0,
    batch_max_bytes: int = 1024 * 1024,
    batch_max_latency: float = 0.05,
    batch_max_messages: int = 100,
) -> pubsub_v1.types.PublishSettings:
    return pubsub_v1.types.PublishSettings(
        timeout=timeout,
        batching=pubsub_v1.types.PublishSettings.BatchSettings(
            max_bytes=batch_max_bytes,
            max_latency=batch_max_latency,
            max_messages=batch_max_messages,
        ),
    )


def build_pull_request(
    subscription: str = None,
    max_messages: int = 1,
) -> pubsub_v1.types.PullRequest:
    sub = subscription_path(subscription)
    return pubsub_v1.types.PullRequest(
        subscription=sub,
        max_messages=max_messages,
    )


def validate_config() -> bool:
    required = [PUBSUB_PROJECT_ID]
    return all(v for v in required)
