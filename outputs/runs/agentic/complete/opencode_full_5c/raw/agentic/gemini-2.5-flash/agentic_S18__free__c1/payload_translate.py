from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    get_project_id,
)
from messaging_models import EventMessage
from google.cloud import translate_v3 as translate
import os


def translate_message_payload(
    subscription_id: str, target_language_code: str = "es", timeout: int = 5
):
    """Consumes a message and translates specified text fields in its payload.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        target_language_code: The BCP-47 language code to translate to (e.g., "es" for Spanish).
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A tuple of (EventMessage, dict) with the translated payload if successful,
        otherwise None.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

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
        original_payload = event_message.data
        translated_payload = original_payload.copy()  # Start with a copy

        print(f"Received message ID: {event_message.id} for translation.")
        print(f"Original payload: {original_payload}")

        text_to_translate = []
        # Example: assume we want to translate a 'message' field if it exists
        if "text" in original_payload and isinstance(original_payload["text"], str):
            text_to_translate.append(original_payload["text"])
        # Add other fields to translate as needed, e.g., if 'description' also needs translation
        if "description" in original_payload and isinstance(
            original_payload["description"], str
        ):
            text_to_translate.append(original_payload["description"])

        if text_to_translate:
            try:
                translation_response = client.translate_text(
                    request={
                        "parent": parent,
                        "contents": text_to_translate,
                        "target_language_code": target_language_code,
                    }
                )

                translated_texts = [
                    t.translated_text for t in translation_response.translations
                ]

                # Apply translated texts back to the payload
                translation_index = 0
                if "text" in translated_payload and isinstance(
                    translated_payload["text"], str
                ):
                    translated_payload["text_translated"] = translated_texts[
                        translation_index
                    ]
                    translation_index += 1
                if "description" in translated_payload and isinstance(
                    translated_payload["description"], str
                ):
                    translated_payload["description_translated"] = translated_texts[
                        translation_index
                    ]
                    translation_index += 1

                print(f"Translated payload: {translated_payload}")
                subscriber.acknowledge(
                    request={"subscription": subscription_path, "ack_ids": [ack_id]}
                )
                return event_message, translated_payload

            except Exception as e:
                print(f"Error translating message {event_message.id}: {e}")
                subscriber.nack(
                    request={"subscription": subscription_path, "ack_ids": [ack_id]}
                )
                return None, None
        else:
            print("No translatable text found in message payload.")
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
            return (
                event_message,
                original_payload,
            )  # Return original if no translation needed
    else:
        print("No messages received for translation.")
        return None, None


if __name__ == "__main__":
    # Example Usage (replace with your actual subscription_id)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Make sure you have Cloud Translation API enabled and permissions set up.
    example_subscription_id = "my-test-subscription"
    example_target_language = "fr"

    # event, translated_data = translate_message_payload(example_subscription_id, example_target_language)
    # if event and translated_data:
    #     print(f"Original Event Data: {event.data}")
    #     print(f"Translated Data: {translated_data}")
