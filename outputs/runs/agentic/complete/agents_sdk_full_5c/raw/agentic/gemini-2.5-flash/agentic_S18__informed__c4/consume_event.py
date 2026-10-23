from messaging_client import get_subscriber_client, get_project_id
import json

def consume_event(subscription_id: str, timeout: int = 5):
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable.")
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        print(f"Attributes: {message.attributes}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except Exception as e:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        print(f"Listening timed out or error occurred: {e}")

