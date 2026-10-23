import os
from google.cloud import pubsub_v1


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_topic_path(topic_id):
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(subscription_id):
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"


TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID", "default-topic")
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "default-subscription")
DEAD_LETTER_TOPIC_ID = os.environ.get("DEAD_LETTER_TOPIC_ID", "dead-letter-topic")

topic_path = get_topic_path(TOPIC_ID)
subscription_path = get_subscription_path(SUBSCRIPTION_ID)
dead_letter_topic_path = get_topic_path(DEAD_LETTER_TOPIC_ID)
