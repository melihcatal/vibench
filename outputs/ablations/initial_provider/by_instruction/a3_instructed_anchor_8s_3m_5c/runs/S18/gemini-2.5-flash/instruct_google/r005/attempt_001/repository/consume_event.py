from messaging_client import get_subscriber_client, get_project_id
import time

def consume_event(subscription_id: str):
    project_id = get_project_id()
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}. Press Ctrl+C to exit.")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=30)  # Blocks indefinitely until an exception is raised or timeout
        except Exception as ex:
            streaming_pull_future.cancel()
            streaming_pull_future.result()  # Re-raise the exception
            raise ex


if __name__ == "__main__":
    # Example usage (replace with your subscription_id)
    example_subscription_id = "your-subscription-id"
    consume_event(example_subscription_id)
