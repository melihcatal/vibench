import os
from google.cloud import pubsub_v1

def _project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID") or os.getenv("GCP_PROJECT")

def get_pubsub_topic_path():
    project = _project_id()
    topic = os.getenv("PUBSUB_TOPIC") or "events"
    return f"projects/{project}/topics/{topic}" if project else topic

def get_subscription_path():
    project = _project_id()
    subscription = os.getenv("PUBSUB_SUBSCRIPTION") or "events-sub"
    return f"projects/{project}/subscriptions/{subscription}" if project else subscription

def get_dead_letter_topic_path():
    project = _project_id()
    topic = os.getenv("PUBSUB_DEAD_LETTER_TOPIC") or "events-dead-letter"
    return f"projects/{project}/topics/{topic}" if project else topic

def get_publisher():
    return pubsub_v1.PublisherClient()

def get_subscriber():
    return pubsub_v1.SubscriberClient()
