import os
import json
from messaging_client import PubSubClient
from typing import Dict, Any, Optional


def consume_event(
    subscription_name: str, timeout: Optional[float] = 5.0
) -> Optional[Dict[str, Any]]:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    client = PubSubClient()
    print(
        f"Attempting to consume message from subscription: {subscription_name} with timeout {timeout}s..."
    )
    message_data = client.consume_message(subscription_name, timeout=timeout)
    if message_data:
        print(f"Successfully consumed message: {message_data.get('data')}")
        return {
            "message_id": message_data.get("message_id"),
            "data": json.loads(message_data.get("data")),  # Assuming JSON data
            "attributes": message_data.get("attributes"),
            "ack_id": message_data.get("ack_id"),
        }
    else:
        print(
            f"No messages consumed from subscription: {subscription_name} within the timeout."
        )
        return None


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file
    # Create a subscription named 'my-test-subscription' to 'my-test-topic' in your Google Cloud project
    # To run this example, ensure you have set up your Google Cloud project and authentication.

    # Make sure to set environment variables:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_subscription_name = os.environ.get(
        "PUBSUB_SUBSCRIPTION_NAME", "my-test-subscription"
    )

    try:
        consumed_message = consume_event(example_subscription_name)
        if consumed_message:
            print(f"Consumed message details: {json.dumps(consumed_message, indent=2)}")
    except Exception as e:
        print(f"Error consuming event: {e}")
