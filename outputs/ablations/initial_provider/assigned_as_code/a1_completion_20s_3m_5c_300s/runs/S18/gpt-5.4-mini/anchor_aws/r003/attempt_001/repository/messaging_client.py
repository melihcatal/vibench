import os

from google.cloud import pubsub_v1


def load_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "topic_path": config.get("topic_path"),
        "subscription_path": config.get("subscription_path"),
        "dead_letter_topic": config.get("dead_letter_topic"),
        "region": config.get("region"),
    }


def publisher_client(config=None):
    _ = load_config(config)
    return pubsub_v1.PublisherClient()


def subscriber_client(config=None):
    _ = load_config(config)
    return pubsub_v1.SubscriberClient()


def topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)


def subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)
