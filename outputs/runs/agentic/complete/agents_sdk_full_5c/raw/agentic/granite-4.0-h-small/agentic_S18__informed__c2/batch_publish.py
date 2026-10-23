import os, uuid
from google.cloud import pubsub_v1

# Helper client utilities imported from local module
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

def batch_publish(topic_name: str, messages: list[dict], attr_prefix: dict = None):
    """Publish a list of events as a batch to a Pub/Sub topic.

    Each dict in `messages` becomes a separate Pub/Sub message.
    An optional attribute prefix can be added to each message.

    Args:
        topic_name (str): Fully qualified topic name.
        messages (list[dict]): List of payload dicts.
        attr_prefix (dict, optional): Attributes to attach to every message.
    """
    client = PubSubClient()
    publisher = pubsub_v1.PublisherClient()
    # Build PubSubMessage objects for each payload
    pub_messages = []
    for payload in messages:
        msg_id = str(uuid.uuid4())
        data = json.dumps(payload).encode('utf-8')
        attrs = attr_prefix.copy() if attr_prefix else None
        attrs.update({"batch_id": msg_id}) if attrs else None
        pub_messages.append(PubSubMessage(data=data, message_id=msg_id, attributes=attrs))
    # The PublisherClient expects raw bytes + attrs; we create a list of tuples
    to_publish = [(msg.data, msg.attributes) for msg in pub_messages]
    # Publish all messages in one call (PublisherClient handles batching internally)
    futures = publisher.publish_many(topic_name, to_publish)
    # Wait for all publishes to succeed
    for fut in futures:
        fut.result()
    print(f"Batch of {len(messages)} messages published to {topic_name}")

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    topic = f"projects/{project_id}/topics/example-batch"
    batch = [
        {"event_id": str(uuid.uuid4()), "action": "order_created", "amount": 42},
        {"event_id": str(uuid.uuid4()), "action": "order_paid", "amount": 42},
    ]
    batch_publish(topic, batch, attr_prefix={"source": "batch_publisher"})
