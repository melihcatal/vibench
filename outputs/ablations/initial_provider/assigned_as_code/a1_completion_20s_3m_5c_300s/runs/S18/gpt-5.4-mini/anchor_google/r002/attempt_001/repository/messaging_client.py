import os

from google.cloud import pubsub_v1


def get_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        "topic_id": config.get("topic_id") or os.environ.get("PUBSUB_TOPIC_ID"),
        "subscription_id": config.get("subscription_id") or os.environ.get("PUBSUB_SUBSCRIPTION_ID"),
        "dead_letter_topic_id": config.get("dead_letter_topic_id") or os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID"),
    }


def publisher_client():
    return pubsub_v1.PublisherClient()


def subscriber_client():
    return pubsub_v1.SubscriberClient()


def topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)


def subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)
