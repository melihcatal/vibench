import os
import json
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the concrete provider
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DLQ_TOPIC_ID = os.getenv('PUBSUB_DLQ_TOPIC_ID')

# Helper function to send a message to a dead‑letter topic
def dead_letter(message: dict, original_msg_id: str) -> str:
    """Publish a failed message to a dead‑letter queue (DLQ) topic.

    Args:
        message (dict): The original payload to re‑publish.
        original_msg_id (str): The ID of the original message for audit.
    Returns:
        str: The ID of the DLQ message.
    """
    publisher = pubsub_v1.PublisherClient()
    dlq_topic_path = publisher.topic_path(PROJECT_ID, DLQ_TOPIC_ID)
    dlq_payload = {"original_msg_id": original_msg_id, "payload": message}
    dlq_data = json.dumps(dlq_payload).encode('utf-8')
    future = publisher.publish(dlq_topic_path, data=dlq_data)
    dlq_msg_id = future.result()
    return dlq_msg_id

def main():
    # Example re‑process of a failed event
    failed_msg = {
        "type": "order_created",
        "order_id": "98765",
        "customer": "bob@example.com"
    }
    original_id = "failed-001"
    dlq_id = dead_letter(failed_msg, original_id)
    print(f"Sent failed message to DLQ with ID: {dlq_id}")

if __name__ == "__main__":
    main()