import os
import google.cloud.pubsub_v1 as pubsub

# Google Cloud Pub/Sub credentials via GOOGLE_APPLICATION_CREDENTIALS
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
subscription_name = os.getenv('PUBSUB_SUBSCRIPTION_NAME')

def consume_event() -> None:
    """Pull a single message from a Pub/Sub subscription and acknowledge it.

    The message payload is expected to be a JSON string that will be decoded
    and printed along with its message ID.
    """
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    
    def callback(message: pubsub.PubsubMessage):
        # Decode JSON payload
        try:
            payload = json.loads(message.data.decode('utf-8'))
            print(f"Received message ID: {message.message_id} - Payload: {payload}")
        except json.JSONDecodeError:
            print(f"Received message ID: {message.message_id} - Non-JSON payload: {message.data}")
        # Acknowledge so it is not redelivered
        message.ack()
        
    # Synchronous pull - block until a message arrives or timeout occurs
    with subscriber:
        subscriber.subscribe(subscription_path, callback=callback)
        # Keep the process alive; in production you might loop or use async flow
        print("Waiting for messages... (press Ctrl+C to exit)")
        try:
            subscriber.poll(timeout=None)
        except KeyboardInterrupt:
            print("Consumer stopped.")
