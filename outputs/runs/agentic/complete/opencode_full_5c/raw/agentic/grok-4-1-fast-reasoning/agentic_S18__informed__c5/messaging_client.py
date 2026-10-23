import os

PUBSUB_CONFIG = {
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
    "topic_id": os.getenv("PUBSUB_TOPIC_ID"),
    "subscription_id": os.getenv("PUBSUB_SUBSCRIPTION_ID"),
    "dead_letter_topic_id": os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID"),
}
