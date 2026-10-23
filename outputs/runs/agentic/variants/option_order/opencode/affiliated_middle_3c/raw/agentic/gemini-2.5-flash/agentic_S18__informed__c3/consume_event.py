import os
from messaging_client import get_subscriber_client

SUBSCRIPTION_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")


def consume_event():
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(
        os.getenv("GOOGLE_CLOUD_PROJECT_ID"), SUBSCRIPTION_ID
    )

    def callback(message):
        print(f"Received message: {message.data}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=30)  # Adjust timeout as needed
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
