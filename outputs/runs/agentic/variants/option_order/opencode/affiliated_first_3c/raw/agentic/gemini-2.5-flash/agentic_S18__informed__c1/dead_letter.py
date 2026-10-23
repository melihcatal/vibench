import os
from messaging_client import PubSubClient
from messaging_models import PubSubMessage, PublishResponse


def send_to_dead_letter(
    dead_letter_topic_id: str, message: PubSubMessage, original_subscription_id: str
) -> PublishResponse:
    client = PubSubClient()
    dead_letter_topic_path = client.publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), dead_letter_topic_id
    )

    attributes = message.attributes if message.attributes else {}
    attributes["original_subscription_id"] = original_subscription_id

    future = client.publisher.publish(
        dead_letter_topic_path, message.data, **attributes
    )
    return PublishResponse(message_ids=[future.result()])


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_id = (
        "my-dead-letter-topic"  # Replace with your dead-letter topic ID
    )
    original_sub_id = (
        "my-test-subscription"  # Replace with your original subscription ID
    )

    failed_message = PubSubMessage(
        data=b'{"error": "processing_failed", "details": "invalid_payload"}',
        attributes={"reason": "payload_error"},
        message_id="failed-message-123",
    )

    try:
        response = send_to_dead_letter(
            dead_letter_topic_id, failed_message, original_sub_id
        )
        print(
            f"Sent failed message to dead-letter topic with ID: {response.message_ids[0]}"
        )
    except Exception as e:
        print(f"Error sending to dead-letter topic: {e}")
