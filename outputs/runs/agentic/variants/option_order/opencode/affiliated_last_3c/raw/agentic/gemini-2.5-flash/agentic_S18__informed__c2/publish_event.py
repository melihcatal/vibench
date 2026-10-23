import os
import json
from messaging_client import PubSubClient
from messaging_models import PubSubMessage


def publish_event(topic_name: str, event_data: dict, attributes: dict = None) -> str:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    message = PubSubMessage(data=event_data, attributes=attributes)
    message_id = client.publish_message(topic_name, message)
    print(f"Published message with ID: {message_id} to topic: {topic_name}")
    return message_id


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file
    # Create a topic named 'my-test-topic' in your Google Cloud project
    # To run this example, ensure you have set up your Google Cloud project and authentication.

    # Make sure to set environment variables:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_topic_name = os.environ.get("PUBSUB_TOPIC_NAME", "my-test-topic")
    example_event_data = {"key": "value", "timestamp": "2023-10-27T10:00:00Z"}
    example_attributes = {"type": "example_event", "source": "script"}

    try:
        message_id = publish_event(
            example_topic_name, example_event_data, example_attributes
        )
        print(f"Successfully published event with ID: {message_id}")
    except Exception as e:
        print(f"Error publishing event: {e}")
