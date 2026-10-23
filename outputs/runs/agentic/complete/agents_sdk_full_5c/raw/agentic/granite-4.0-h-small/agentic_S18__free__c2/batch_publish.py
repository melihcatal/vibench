import os
import json
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the concrete provider
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
TOPIC_ID = os.getenv('PUBSUB_TOPIC_ID')

# Helper function to publish a batch of messages with attributes
def batch_publish(messages: list[dict]) -> list[str]:
    """Publish a list of messages as a batch to Pub/Sub.

    Each message must contain an 'id' field that will be used as an attribute.
    Returns a list of resulting message IDs.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    batch_futures = []
    for msg in messages:
        if 'id' not in msg:
            raise ValueError(f"Message missing required 'id' attribute: {msg}")
        # Include the id as a Pub/Sub attribute
        attributes = {'msg_id': msg['id']}
        data = json.dumps(msg).encode('utf-8')
        future = publisher.publish(topic_path, data=data, **attributes)
        batch_futures.append(future)
    # Wait for all publishes to complete and collect IDs
    msg_ids = [f.result() for f in batch_futures]
    return msg_ids

def main():
    sample_batch = [
        {"id": "batch-001", "type": "click", "user": "alice"},
        {"id": "batch-002", "type": "view", "user": "bob"},
        {"id": "batch-003", "type": "purchase", "user": "alice", "amount": 19.99}
    ]
    ids = batch_publish(sample_batch)
    print(f"Published batch, IDs: {ids}")

if __name__ == "__main__":
    main()