import os
from concurrent.futures import TimeoutError

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

from messaging_client import get_subscriber_client, get_subscription_path

def consume_one_message(subscriber: pubsub_v1.SubscriberClient, subscription_path: str):
    """Consumes a single message from a Pub/Sub subscription."""
    
    ack_ids = []
    message_data = None

    try:
        response = subscriber.pull(subscription=subscription_path, max_messages=1, return_immediately=True)
        
        if not response.received_messages:
            print("No messages received.")
            return None

        received_message = response.received_messages[0]
        ack_ids.append(received_message.ack_id)
        
        message_data = received_message.message.data.decode("utf-8")
        print(f"Received message: {message_data}")

        if ack_ids:
            subscriber.acknowledge(subscription=subscription_path, ack_ids=ack_ids)
            print(f"Acknowledged message(s) for subscription {subscription_path}.")
        
        return message_data

    except GoogleAPICallError as e:
        print(f"Error consuming message from {subscription_path}: {e}")
        # Not acknowledging the message so it can be redelivered.
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment
    # Required environment variables: GOOGLE_PROJECT_ID, MY_SUBSCRIPTION_ID
    subscription_id = os.environ.get("MY_SUBSCRIPTION_ID")
    if subscription_id:
        client = get_subscriber_client()
        path = get_subscription_path(subscription_id)
        consume_one_message(client, path)
    else:
        print("MY_SUBSCRIPTION_ID environment variable not set. Skipping example.")
