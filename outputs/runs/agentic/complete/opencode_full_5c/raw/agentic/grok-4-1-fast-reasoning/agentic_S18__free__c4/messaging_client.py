import os

PUBSUB_PROJECT_ID: str = os.getenv("PUBSUB_PROJECT_ID", "your-project-id")
PUBSUB_TOPIC: str = os.getenv("PUBSUB_TOPIC", "events-topic")
PUBSUB_SUBSCRIPTION: str = os.getenv("PUBSUB_SUBSCRIPTION", "events-subscription")
PUBSUB_DEADLETTER_TOPIC: str = os.getenv("PUBSUB_DEADLETTER_TOPIC", "events-deadletter")
