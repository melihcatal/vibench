import os
from google.cloud import pubsub_v1
from google.protobuf import duration_pb2

# Use Google Cloud Pub/Sub as the managed messaging service
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_NAME = os.getenv('PUBSUB_TOPIC', 'my-topic')

# Helper utilities from local helpers
from messaging_client import get_publisher_client
from messaging_models import build_event_message

def batch_publish(events):
    """Publish a list of event dictionaries as a batch to Pub/Sub.

    Args:
        events (list[dict]): Each dict is a payload representing one message.
    """
    publisher = get_publisher_client()
    messages = []
    for i, evt in enumerate(events, start=1):
        msg = build_event_message(evt, f'batch-{i}')
        messages.append((msg,))  # single-arg tuple required by publish_batch
    future = publisher.publish_batch(TOPIC_NAME, messages)
    try:
        response = future.result()
        print(f'Batch published {len(response)} messages.')
    except Exception as e:
        print(f'Error in batch publish: {e}')

def main():
    batch = [
        {'user_id': '1', 'action': 'view', 'page': '/'},
        {'user_id': '2', 'action': 'click', 'page': '/product'},
        {'user_id': '3', 'action': 'search', 'keyword': 'phone'}
    ]
    batch_publish(batch)

if __name__ == '__main__':
    main()
