import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_ID = os.getenv('TOPIC_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')
DEAD_LETTER_TOPIC_ID = os.getenv('DEAD_LETTER_TOPIC_ID')

publisher_client = pubsub_v1.PublisherClient()
subscriber_client = pubsub_v1.SubscriberClient()

def get_topic_path(topic_id: str = TOPIC_ID) -> str:
    if not PROJECT_ID:
        raise ValueError('GOOGLE_CLOUD_PROJECT env var required')
    return publisher_client.topic_path(PROJECT_ID, topic_id)

def get_subscription_path(sub_id: str = SUBSCRIPTION_ID) -> str:
    if not PROJECT_ID:
        raise ValueError('GOOGLE_CLOUD_PROJECT env var required')
    return subscriber_client.subscription_path(PROJECT_ID, sub_id)