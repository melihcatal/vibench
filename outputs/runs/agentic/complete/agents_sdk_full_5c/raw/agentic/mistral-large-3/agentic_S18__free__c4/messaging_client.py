import os
from google.cloud import pubsub_v1

def get_pubsub_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

def get_pubsub_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()

def load_messaging_config():
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "topic_id": os.getenv("PUBSUB_TOPIC_ID", "events-topic"),
        "subscription_id": os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription"),
        "dead_letter_topic_id": os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic")
    }