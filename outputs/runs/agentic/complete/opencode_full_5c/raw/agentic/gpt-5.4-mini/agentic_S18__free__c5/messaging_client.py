import os
from dataclasses import dataclass
from google.cloud import pubsub_v1


@dataclass
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str


def load_messaging_config():
    return MessagingConfig(project_id=os.environ['GOOGLE_CLOUD_PROJECT'], topic_id=os.environ.get('PUBSUB_TOPIC', 'events'), subscription_id=os.environ.get('PUBSUB_SUBSCRIPTION', 'events-sub'), dead_letter_topic_id=os.environ.get('PUBSUB_DEAD_LETTER_TOPIC', 'events-dlq'))


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_topic_path(client, project_id, topic_id):
    return client.topic_path(project_id, topic_id)


def get_subscription_path(client, project_id, subscription_id):
    return client.subscription_path(project_id, subscription_id)
