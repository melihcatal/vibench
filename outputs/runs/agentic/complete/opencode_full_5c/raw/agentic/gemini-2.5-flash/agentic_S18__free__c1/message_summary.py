from messaging_client import get_subscriber_client, get_subscription_path, get_project_id
from messaging_models import EventMessage
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os

def summarize_message_content(subscription_id: str, timeout: int = 5):
    """Consumes a message and summarizes its content using Vertex AI.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A tuple of (EventMessage, str) if a message is consumed and summarized,
        otherwise None.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize Vertex AI
    vertexai.init(project=project_id, location="us-central1") # Use an appropriate region
    model = TextGenerationModel.from_pretrained("gemini-pro") # Concrete model identifier

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
        message_text = str(event_message.data) # Convert data to string for summarization

        print(f"Received message ID: {event_message.id} for summarization.")

        try:
            prompt = f"Summarize the following text:

            {message_text}

            Summary:"

            parameters = {
                "temperature": 0.2,
                "max_output_tokens": 256,
                "top_p": 0.8,
                "top_k": 40
            }
            summary = model.predict(prompt, **parameters).text
            print(f"Generated Summary: {summary}")

            subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})
            return event_message, summary

        except Exception as e:
            print(f"Error summarizing message {event_message.id}: {e}")
            # Nack the message or send to DLQ if appropriate for retry/dead-lettering
            subscriber.nack(request={"subscription": subscription_path, "ack_ids": [ack_id]})
            return None, None
    else:
        print("No messages received for summarization.")
        return None, None

if __name__ == '__main__':
    # Example Usage (replace with your actual subscription_id)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Make sure you have Vertex AI API enabled and permissions set up.
    example_subscription_id = "my-test-subscription"

    # event, summary = summarize_message_content(example_subscription_id)
    # if event and summary:
    #     print(f"Original Event Data: {event.data}")
    #     print(f"Summary: {summary}")
