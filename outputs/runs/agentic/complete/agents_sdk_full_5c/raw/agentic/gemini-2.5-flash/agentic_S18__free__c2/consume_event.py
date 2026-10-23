from google.cloud import pubsub_v1
import os
import json
import concurrent.futures

def consume_one_message(project_id: str, subscription_id: str, timeout: float = 5.0) -> dict | None:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    pulled_message = None

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        nonlocal pulled_message
        try:
            pulled_message = json.loads(message.data.decode("utf-8"))
            message.ack()
        except Exception as e:
            print(f"Error processing message: {e}")
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # Block until a message is received or timeout occurs
            streaming_pull_future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            return None
        except Exception as e:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            raise e

    return pulled_message

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "my-event-subscription")
    
    # print(f"Consuming one message from {SUBSCRIPTION_ID}...")
    # message = consume_one_message(PROJECT_ID, SUBSCRIPTION_ID, timeout=10)
    # if message:
    #     print(f"Received message: {message}")
    # else:
    #     print("No message received within the timeout period.")
