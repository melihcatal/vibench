import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = "my-topic"
SUBSCRIPTION_ID = "my-subscription"
DEAD_LETTER_TOPIC_ID = "my-dead-letter-topic"


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_topic_path(publisher_client, project_id, topic_id):
    return publisher_client.topic_path(project_id, topic_id)


def get_subscription_path(subscriber_client, project_id, subscription_id):
    return subscriber_client.subscription_path(project_id, subscription_id)
