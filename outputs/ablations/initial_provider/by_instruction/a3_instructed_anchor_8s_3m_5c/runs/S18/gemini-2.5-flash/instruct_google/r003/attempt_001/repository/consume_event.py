from google.cloud import pubsub_v1
import os

def consume_event(project_id: str, subscription_id: str) -> dict or None:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1})

    if response.received_messages:
        message = response.received_messages[0].message
        
        # Acknowledge the message to remove it from the subscription
        ack_ids = [response.received_messages[0].ack_id]
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
        
        return {
            "data": message.data.decode("utf-8"),
            "attributes": dict(message.attributes),
            "message_id": message.message_id,
        }
    return None

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    SUBSCRIPTION_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")

    if not PROJECT_ID or not SUBSCRIPTION_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        message = consume_event(PROJECT_ID, SUBSCRIPTION_ID)
        if message:
            print(f"Consumed message: {message}")
        else:
            print("No messages to consume.")
