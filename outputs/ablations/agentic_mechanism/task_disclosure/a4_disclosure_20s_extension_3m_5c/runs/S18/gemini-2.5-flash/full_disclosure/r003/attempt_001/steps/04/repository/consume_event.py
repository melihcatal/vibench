from google.cloud import pubsub_v1
import os

def consume_event(project_id: str, subscription_id: str) -> dict:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        project_id: The Google Cloud project ID.
        subscription_id: The ID of the Pub/Sub subscription.

    Returns:
        A dictionary containing the message data and attributes, or None if no message is received.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True},
        timeout=5.0  # Optional: set a timeout for the pull request
    )

    if response.received_messages:
        message = response.received_messages[0].message
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [response.received_messages[0].ack_id]}
        )
        return {
            "data": message.data.decode("utf-8"),
            "attributes": dict(message.attributes)
        }
    return None

if __name__ == "__main__":
    # Replace with your actual Google Cloud project ID and subscription ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_SUBSCRIPTION_ID environment variables.")
    else:
        print(f"Attempting to consume message from subscription: {subscription_id} in project: {project_id}")
        message = consume_event(project_id, subscription_id)
        if message:
            print("Received message:")
            print(f"Data: {message['data']}")
            print(f"Attributes: {message['attributes']}")
        else:
            print("No messages received.")
