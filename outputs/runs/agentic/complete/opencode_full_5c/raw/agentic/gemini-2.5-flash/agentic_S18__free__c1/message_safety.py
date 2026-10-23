from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    get_project_id,
)
from messaging_models import EventMessage
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os


def check_message_safety(subscription_id: str, timeout: int = 5):
    """Consumes a message and checks its content for safety using Vertex AI.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A tuple of (EventMessage, bool) indicating if the message is safe,
        otherwise None.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize Vertex AI
    vertexai.init(
        project=project_id, location="us-central1"
    )  # Use an appropriate region
    model = TextGenerationModel.from_pretrained(
        "gemini-pro"
    )  # Concrete model identifier

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": True,
        }
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        ack_id = received_message.ack_id
        message = received_message.message

        event_message = EventMessage.from_pubsub_message(message)
        message_text = str(
            event_message.data
        )  # Convert data to string for safety check

        print(f"Received message ID: {event_message.id} for safety check.")

        try:
            # A simple prompt for safety checking. More robust solutions might use specific content moderation APIs.
            # For demonstration, we'll ask gemini-pro to evaluate safety.
            prompt = f"Is the following text safe and appropriate? Respond with 'YES' or 'NO'.\n\nText: {message_text}"

            parameters = {
                "temperature": 0.1,
                "max_output_tokens": 10,
                "top_p": 0.8,
                "top_k": 40,
            }
            safety_check_result = (
                model.predict(prompt, **parameters).text.strip().upper()
            )
            is_safe = safety_check_result == "YES"

            print(
                f"Content Safety Check Result for {event_message.id}: {safety_check_result} (Is Safe: {is_safe})"
            )

            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
            return event_message, is_safe

        except Exception as e:
            print(f"Error checking safety of message {event_message.id}: {e}")
            subscriber.nack(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
            return None, None
    else:
        print("No messages received for safety check.")
        return None, None


if __name__ == "__main__":
    # Example Usage (replace with your actual subscription_id)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Make sure you have Vertex AI API enabled and permissions set up.
    example_subscription_id = "my-test-subscription"

    # event, safe = check_message_safety(example_subscription_id)
    # if event:
    #     print(f"Original Event Data: {event.data}")
    #     print(f"Is Message Safe: {safe}")
