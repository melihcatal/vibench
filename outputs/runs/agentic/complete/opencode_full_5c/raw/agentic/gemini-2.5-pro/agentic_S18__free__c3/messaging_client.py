import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_project_id():
    return os.environ.get("GCP_PROJECT", "your-gcp-project-id")


def get_topic_path(topic_id):
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(subscription_id):
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def create_topic_if_not_exists(topic_id):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)
    try:
        publisher.get_topic(topic=topic_path)
    except NotFound:
        publisher.create_topic(name=topic_path)
    return topic_path


def create_subscription_if_not_exists(
    topic_id, subscription_id, dead_letter_topic_id=None
):
    subscriber = get_subscriber_client()
    topic_path = get_topic_path(topic_id)
    subscription_path = get_subscription_path(subscription_id)

    dead_letter_policy = None
    if dead_letter_topic_id:
        dead_letter_topic_path = create_topic_if_not_exists(dead_letter_topic_id)
        dead_letter_policy = pubsub_v1.types.DeadLetterPolicy(
            dead_letter_topic=dead_letter_topic_path,
            max_delivery_attempts=5,
        )

    try:
        subscriber.get_subscription(subscription=subscription_path)
    except NotFound:
        subscriber.create_subscription(
            name=subscription_path,
            topic=topic_path,
            dead_letter_policy=dead_letter_policy,
        )
    return subscription_path
