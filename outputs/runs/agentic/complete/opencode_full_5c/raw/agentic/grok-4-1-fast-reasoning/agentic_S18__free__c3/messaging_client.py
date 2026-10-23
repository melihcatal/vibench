import os
from google.cloud import pubsub_v1

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
if not GCP_PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID environment variable is required")

TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic")

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

TOPIC_PATH = publisher.topic_path(GCP_PROJECT_ID, TOPIC_ID)
SUBSCRIPTION_PATH = subscriber.subscription_path(GCP_PROJECT_ID, SUBSCRIPTION_ID)
DEAD_LETTER_TOPIC_PATH = publisher.topic_path(GCP_PROJECT_ID, DEAD_LETTER_TOPIC_ID)
