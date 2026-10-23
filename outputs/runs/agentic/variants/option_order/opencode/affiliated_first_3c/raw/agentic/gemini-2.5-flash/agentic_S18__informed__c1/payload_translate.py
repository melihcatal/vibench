import os
from typing import Dict, Any
from messaging_client import TranslationClient
from messaging_models import Event


def translate_message_payload(
    event: Event, target_language_code: str = "es"
) -> Dict[str, Any]:
    client = TranslationClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    parent = f"projects/{project_id}/locations/global"

    translated_payload = {}
    for key, value in event.payload.items():
        if isinstance(value, str):
            response = client.client.translate_text(
                request={
                    "parent": parent,
                    "contents": [value],
                    "target_language_code": target_language_code,
                }
            )
            translated_payload[key] = response.translations[0].translated_text
        else:
            translated_payload[key] = value  # Keep non-string values as is

    return translated_payload


if __name__ == "__main__":
    # Example usage
    sample_event = Event(
        event_id="translate-test-1",
        event_type="customer_feedback",
        payload={
            "customer_name": "John Doe",
            "feedback_text": "I love your product, it's very useful!",
        },
    )

    try:
        translated_payload = translate_message_payload(
            sample_event, target_language_code="fr"
        )
        print(f"Original payload: {sample_event.payload}")
        print(f"Translated payload (French): {translated_payload}")
    except Exception as e:
        print(f"Error translating message payload: {e}")
