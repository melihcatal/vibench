import os
from dataclasses import dataclass
from google.cloud import pubsub_v1

@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_path: str
    subscription_path: str
    dead_letter_topic: str

def get_pubsub_config():
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    topic = os.environ.get('PUBSUB_TOPIC', f'projects/{project_id}/topics/events')
    subscription = os.environ.get('PUBSUB_SUBSCRIPTION', f'projects/{project_id}/subscriptions/events-sub')
    dead_letter_topic = os.environ.get('PUBSUB_DEAD_LETTER_TOPIC', f'projects/{project_id}/topics/dead-letter')
    return PubSubConfig(project_id=project_id, topic_path=topic, subscription_path=subscription, dead_letter_topic=dead_letter_topic)

def get_publisher(cfg):
    return pubsub_v1.PublisherClient()

def get_subscriber(cfg):
    return pubsub_v1.SubscriberClient()
