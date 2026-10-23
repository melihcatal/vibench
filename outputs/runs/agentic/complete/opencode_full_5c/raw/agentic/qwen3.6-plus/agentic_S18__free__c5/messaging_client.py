import os
from google.cloud import pubsub_v1
from google.api_core import retry


def get_publisher_client() -> pubsub_v1.PublisherClient:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=False,
    )
    batch_settings = pubsub_v1.types.BatchSettings(
        max_latency=0.05,
    )
    if credentials_path:
        return pubsub_v1.PublisherClient(
            publisher_options=publisher_options, batch_settings=batch_settings
        )
    return pubsub_v1.PublisherClient(
        publisher_options=publisher_options, batch_settings=batch_settings
    )


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    flow_control = pubsub_v1.types.FlowControl(
        max_messages=10,
    )
    return pubsub_v1.SubscriberClient(flow_control=flow_control)


def get_topic_path(project_id: str, topic_id: str) -> str:
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(project_id: str, subscription_id: str) -> str:
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def create_subscription_if_not_exists(
    project_id: str,
    topic_id: str,
    subscription_id: str,
    dead_letter_topic_id: str = None,
    max_delivery_attempts: int = 5,
):
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)
    topic_path = get_topic_path(project_id, topic_id)

    try:
        subscription = subscriber.get_subscription(subscription=subscription_path)
        return subscription
    except Exception:
        subscription_config = {
            "name": subscription_path,
            "topic": topic_path,
            "ack_deadline_seconds": 60,
        }

        if dead_letter_topic_id:
            dlq_topic_path = get_topic_path(project_id, dead_letter_topic_id)
            subscription_config["dead_letter_policy"] = {
                "dead_letter_topic": dlq_topic_path,
                "max_delivery_attempts": max_delivery_attempts,
            }

        subscription = subscriber.create_subscription(request=subscription_config)
        return subscription


def get_pubsub_config() -> dict:
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project"),
        "topic_id": os.environ.get("PUBSUB_TOPIC_ID", "events-topic"),
        "subscription_id": os.environ.get(
            "PUBSUB_SUBSCRIPTION_ID", "events-subscription"
        ),
        "dlq_topic_id": os.environ.get("PUBSUB_DLQ_TOPIC_ID", "events-dead-letter"),
        "api_endpoint": "pubsub.googleapis.com",
        "provider": "google-cloud-pubsub",
    }
