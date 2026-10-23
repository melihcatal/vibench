from google.cloud import pubsub_v1
import os
import json

def consume_one_event(project_id: str, subscription_id: str, timeout: int = 5):
    """Consumes one message from a Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        print("No messages received within the timeout period.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"Listening for messages on {subscription_path} threw an exception: {e}.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    finally:
        subscriber.api.transport.close()

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    subscription_id = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID_CONSUME")

    if not all([project_id, subscription_id]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID_CONSUME environment variables.")
    else:
        consume_one_event(project_id, subscription_id)
