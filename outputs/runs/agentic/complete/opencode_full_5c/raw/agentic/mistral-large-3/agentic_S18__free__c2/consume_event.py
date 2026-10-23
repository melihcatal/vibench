from google.cloud import pubsub_v1
import os
import json

# Provider: Google Cloud Pub/Sub
# Identifiable by: google.cloud.pubsub_v1, GOOGLE_APPLICATION_CREDENTIALS
subscriber = pubsub_v1.SubscriberClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
SUBSCRIPTION_NAME = os.getenv("PUBSUB_SUBSCRIPTION_NAME", "events-subscription")


def consume_event() -> dict:
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    response = subscriber.pull(
        subscription_path, max_messages=1, return_immediately=True
    )

    if not response.received_messages:
        return None

    message = response.received_messages[0]
    data = json.loads(message.message.data.decode("utf-8"))
    subscriber.acknowledge(subscription_path, [message.ack_id])

    return data
