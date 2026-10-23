import os

PUBSUB_PROJECT_ID = os.getenv("PUBSUB_PROJECT_ID", "your-project-id")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
PUBSUB_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
PUBSUB_DLQ_TOPIC_ID = os.getenv("PUBSUB_DLQ_TOPIC_ID", "events-dlq-topic")