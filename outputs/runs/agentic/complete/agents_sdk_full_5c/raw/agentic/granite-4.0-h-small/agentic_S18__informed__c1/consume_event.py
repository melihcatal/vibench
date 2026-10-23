import os
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the managed messaging service
# Environment variable points to the credentials
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
SUBSCRIPTION_NAME = os.getenv('PUBSUB_SUBSCRIPTION', 'my-sub')

# Helper utilities from local helpers
from messaging_client import get_subscriber_client
from messaging_models import normalize_message

def consume_event(max_messages: int = 1):
    """Pull up to `max_messages` messages from the subscription and acknowledge them.

    Args:
        max_messages (int): Maximum number of messages to retrieve in a single call.
    """
    subscriber = get_subscriber_client()
    future = subscriber.pull(subscription=SUBSCRIPTION_NAME, max_messages=max_messages)
    response = future.result()
    if not response.received_messages:
        print('No messages available.')
        return []
    messages = []
    for received in response.received_messages:
        # Decode and normalize payload
        payload = normalize_message(received.message.data)
        # Acknowledge after processing
        subscriber.acknowledge(subscription=SUBSCRIPTION_NAME, ack_ids=[received.ack_id])
        messages.append(payload)
        print(f'Consumed message: {payload}')
    return messages

def main():
    msgs = consume_event(max_messages=5)
    print(f'Consumed {len(msgs)} messages.')

if __name__ == '__main__':
    main()
