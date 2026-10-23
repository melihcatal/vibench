from google.cloud import pubsub_v1
import os


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)


def get_subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)


TOPIC_ID = "my-topic"
SUBSCRIPTION_ID = "my-subscription"
DEAD_LETTER_TOPIC_ID = "my-dead-letter-topic"
