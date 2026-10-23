from google.cloud import pubsub_v1
import os


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_topic_path(topic_id):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(subscription_id):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def get_dead_letter_topic_path():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_id = os.getenv("DEAD_LETTER_TOPIC_ID", "dead-letter-topic")
    return f"projects/{project_id}/topics/{dead_letter_topic_id}"
