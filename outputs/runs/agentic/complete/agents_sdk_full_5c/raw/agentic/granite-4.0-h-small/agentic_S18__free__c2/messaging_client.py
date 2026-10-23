import os
import json
from .messaging_models import PubSubMessage, format_response, normalize_message
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the concrete provider
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
SUBSCRIPTION_ID = os.getenv('PUBSUB_SUBSCRIPTION_ID')

# Helper client utilities
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Create and return a Pub/Sub subscriber client.",
    return pubsub_v1.SubscriberClient()


def pull_subscription_messages(max_msgs: int = 1, timeout_seconds: float = 10.0) -> list[PubSubMessage]:
    """Pull messages from a subscription and normalize them.",
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    response = subscriber.pull(subscription_path, max_messages=max_msgs, timeout=timeout_seconds)
    normalized = []
    if response.received_messages:
        for msg in response.received_messages:
            normalized.append(normalize_message(msg.message))
        # Acknowledge all pulled messages
        subscriber.acknowledge(subscription_path, [m.ack_id for m in response.received_messages])
    return normalized


def publish_event(event: dict) -> str:
    """Publish a single JSON event to a Pub/Sub topic.",
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, os.getenv('PUBSUB_TOPIC_ID'))
    data = json.dumps(event).encode('utf-8')
    future = publisher.publish(topic_path, data=data)
    return future.result()


def send_dead_letter(original_msg_id: str, payload: dict) -> str:
    """Send a failed message to a dead-letter topic.",
    publisher = pubsub_v1.PublisherClient()
    dlq_topic = os.getenv('PUBSUB_DLQ_TOPIC_ID')
    dlq_path = publisher.topic_path(PROJECT_ID, dlq_topic)
    dlq_payload = {
        'original_msg_id': original_msg_id,
        'payload': payload
    }
    dlq_data = json.dumps(dlq_payload).encode('utf-8')
    future = publisher.publish(dlq_path, data=dlq_data)
    return future.result()


def process_messages() -> list[PubSubResponse]:
    """Example workflow: pull, normalize, and return response for each message.",
    raw_msgs = pull_subscription_messages()
    responses = []
    for raw in raw_msgs:
        norm = normalize_message(raw)
        # Example validation: ensure payload contains 'type'
        if 'type' not in norm['data']:
            err = "Missing 'type' field"
            # Push to DLQ
            dlq_id = send_dead_letter(norm['id'], norm['data'])
            responses.append(format_response(False, err, None, err))
        else:
            responses.append(format_response(True, f"Processed {norm['id']}", norm))
    return responses


def main():
    results = process_messages()
    for r in results:
        print(json.dumps(r, indent=2))

if __name__ == "__main__":
    main()