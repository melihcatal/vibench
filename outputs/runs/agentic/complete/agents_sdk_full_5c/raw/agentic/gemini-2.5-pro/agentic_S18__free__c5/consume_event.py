
import os
import time
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client

def consume_one_message():
    """
    Consumes a single message from a Google Cloud Pub/Sub subscription.
    """
    subscriber = get_subscriber_client()
    project_id = os.environ["GCP_PROJECT_ID"]
    subscription_id = os.environ["GCP_SUBSCRIPTION_ID"]
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # We will pull just one message for this example.
    # The subscriber is asynchronous, so we'll use a future to wait for a result.
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=lambda message: message.ack())
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap the subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `one()` is called, it will block until a message is received.
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 1},
                retry=None,
                timeout=15,
            )
            if not response.received_messages:
                print("No message received.")
                return None
            
            received_message = response.received_messages[0]
            print(f"Received message: {received_message.message.data.decode('utf-8')}")
            
            # Acknowledge the message so it's not delivered again.
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
            )
            print(f"Acknowledged message: {received_message.ack_id}")
            return received_message.message.data
            
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            print("Timeout waiting for message.")
            return None
        except Exception as e:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            print(f"An error occurred: {e}")
            return None

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variables before running:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_SUBSCRIPTION_ID="your-subscription-id"
    # consume_one_message()
    pass
