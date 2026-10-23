import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_subscription_path

def consume_one_message():
    """Consumes and acknowledges a single message from a Pub/Sub subscription."""
    subscriber, subscription_path = get_subscriber_client()
    
    message_data = None
    
    def callback(message):
        nonlocal message_data
        print(f"Received message: {message.data.decode('utf-8')}")
        message_data = message.data.decode('utf-8')
        message.ack()
        # Stop the subscriber after receiving one message
        streaming_pull_future.cancel()
        streaming_pull_future.result()


    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")

    try:
        # Wait for the first message
        streaming_pull_future.result(timeout=30)
    except TimeoutError:
        print("Timeout reached, no message received.")
        streaming_pull_future.cancel()
        streaming_pull_future.result() # Block until the shutdown is complete
    
    subscriber.close()
    return message_data

if __name__ == '__main__':
    if os.getenv("GCP_PROJECT_ID"):
        consumed_message = consume_one_message()
        if consumed_message:
            print(f"\nSuccessfully consumed message: {consumed_message}")
        else:
            print("\nNo message consumed.")
    else:
        print("Set GCP_PROJECT_ID and other env vars to run.")
