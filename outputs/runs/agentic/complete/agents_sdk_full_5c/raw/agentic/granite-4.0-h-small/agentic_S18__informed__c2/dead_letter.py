import os
from google.cloud import pubsub_v1

# Helper client utilities imported from local module
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

def dead_letter(message: PubSubMessage, dlq_topic: str):
    """Move a failed Pub/Sub message to a dead‑letter topic.

    Args:
        message (PubSubMessage): The original message wrapper containing the ack ID.
        dlq_topic (str): Fully qualified dead‑letter topic name.
    """
    client = PubSubClient()
    subscriber = pubsub_v1.SubscriberClient()
    # Re‑publish the same data to the DLQ topic
    data = message.data  # raw bytes already stored in the wrapper
    attributes = message.attributes or {}
    dlq_msg = pubsub_v1.types.PubsubMessage(data=data, attributes=attributes)
    publish_future = client.publish(dlq_topic, dlq_msg)
    publish_future.result()  # wait for publish to finish
    print(f"Dead‑lettered message id={message.message_id} to {dlq_topic}")
    # Ack original message so it is not retried indefinitely
    message.ack()

if __name__ == "__main__":
    # Example usage
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    dlq_topic = f"projects/{project_id}/topics/example-dlq"
    # In practice you would obtain a PubSubMessage from your error handling path
    # Here we simulate with dummy data
    dummy_msg = PubSubMessage(data=b"failed payload", message_id="sim-123")
    dead_letter(dummy_msg, dlq_topic)
