import json
from google.cloud import pubsub_v1
from typing import List, Dict
from messaging_models import MessagePayload
from messaging_client import get_publisher_client

PROJECT_ID = 'your-gcp-project-id'
TOPIC_ID = 'your-topic-id'

def batch_publish(events: List[Dict[str, any]]) -> List[str]:
    """Publish a list of JSON events as a batch to a Pub/Sub topic.

    Args:
        events (List[Dict]): Each dict represents an event payload.
    Returns:
        List[str]: The message IDs returned by Pub/Sub.
    """
    publisher = get_publisher_client()
    messages = []
    for ev in events:
        payload = MessagePayload(**ev)
        data = json.dumps(payload.dict()).encode('utf-8')
        # Allow client to assign a custom ID or let Pub/Sub generate one
        msg = publisher.publish(TOPIC_ID, data=data)
        messages.append(msg)
    print(f"Batch published {len(messages)} messages.")
    return [msg.result() for msg in messages]  # blocking wait for ack IDs

if __name__ == '__main__':
    sample_batch = [
        {"event_id": "batch-001", "timestamp": "2025-08-14T12:00:00Z", "data": {"key": "value1"}},
        {"event_id": "batch-002", "timestamp": "2025-08-14T12:01:00Z", "data": {"key": "value2"}}
    ]
    batch_publish(sample_batch)
