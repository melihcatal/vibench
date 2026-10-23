import os

from google.cloud import pubsub_v1


def load_config(config=None):
    config = dict(config or {})
    if "project_id" not in config:
        config["project_id"] = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    return config


def publisher_client():
    return pubsub_v1.PublisherClient()


def subscriber_client():
    return pubsub_v1.SubscriberClient()


def topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)


def subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)
