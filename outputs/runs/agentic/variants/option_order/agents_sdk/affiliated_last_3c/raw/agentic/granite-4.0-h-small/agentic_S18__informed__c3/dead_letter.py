import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import DeadLetterPayload

def send_to_dead_letter(source_subscription, dead_letter_topic):
    """Move messages from a source subscription to a dead-letter topic.",
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    subscriber = get_pubsub_client()
    publisher = get_pubsub_client()
    source_path = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/subscriptions/{source_subscription}"
    dl_topic_path = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/topics/{dead_letter_topic}"
    # Pull messages with a lease
    request = {
        "subscription": source_path,
        "max_messages": 10,
    }
    response = subscriber.pull(request)
    received_messages = response.received_messages
    if not received_messages:
        print("No messages to move.")
        return
    for rm in received_messages:
        # Re-publish to dead-letter topic
        message_data = rm.message.data
        metadata = {
            "original_message_id": rm.message.message_id,
            "original_sub": source_subscription,
        }
        dl_payload = DeadLetterPayload(original_message=rm.message.data.decode('utf-8'), metadata=metadata).to_json()
        publisher.publish(dl_topic_path, data=dl_payload.encode('utf-8'))
        print(f"Moved message {rm.message.message_id} to dead-letter topic.")
        # Ack the original message
        subscriber.acknowledge(source_path, [rm.ack_id])
