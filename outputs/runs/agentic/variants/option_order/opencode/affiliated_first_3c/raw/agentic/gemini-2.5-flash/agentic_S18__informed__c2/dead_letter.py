import json
import os

from messaging_client import PubSubClient
from messaging_models import PubsubMessage, DeadLetterRequest, DeadLetterResponse


def dead_letter(
    dead_letter_topic_id: str, request: DeadLetterRequest
) -> DeadLetterResponse:
    client = PubSubClient()
    dead_letter_topic_path = client.get_topic_path(dead_letter_topic_id)

    # Add a reason for dead-lettering as an attribute
    attributes = request.message.attributes.copy()
    attributes["dead_letter_reason"] = request.reason

    future = client.publisher.publish(
        dead_letter_topic_path, request.message.data, **attributes
    )
    future.result()  # Wait for the publish operation to complete

    return DeadLetterResponse(success=True)


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT environment variable set)
    # and a Pub/Sub topic named 'my-dead-letter-topic'
    dead_letter_topic_id = "my-dead-letter-topic"

    failed_event_data = {"error": "processing_failed", "original_message": "some_data"}
    failed_message_attributes = {"original_topic": "my-topic", "attempt": "3"}

    failed_message = PubsubMessage(
        data=json.dumps(failed_event_data).encode("utf-8"),
        attributes=failed_message_attributes,
    )

    request = DeadLetterRequest(
        message=failed_message, reason="Failed to process after multiple retries"
    )
    response = dead_letter(dead_letter_topic_id, request)

    if response.success:
        print("Message successfully sent to dead-letter topic.")
    else:
        print("Failed to send message to dead-letter topic.")
