from google.cloud import pubsub_v1
import os

# Set your Google Cloud Project ID and Subscription Name
# You can set these as environment variables or replace them directly
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
subscription_id = os.environ.get("GOOGLE_CLOUD_SUBSCRIPTION_ID")

if not project_id or not subscription_id:
    print("Please set the GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_SUBSCRIPTION_ID environment variables or hardcode them in the script.")
    exit(1)

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def consume_message():
    print(f"Listening for messages on {subscription_path}...")

    # The `sub_client.subscribe` method is asynchronous, so we will use a Future to block until a message is received.
    # We are pulling only one message at a time to fulfill the task requirement of "consumes one message".
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True}
    )

    if response.received_messages:
        for received_message in response.received_messages:
            message_data = received_message.message.data.decode("utf-8")
            print(f"Received message: {message_data}")
            # Acknowledge the message to remove it from the subscription
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
            )
            print(f"Acknowledged message: {received_message.ack_id}")
    else:
        print("No messages received.")

    subscriber.close()

if __name__ == "__main__":
    consume_message()
