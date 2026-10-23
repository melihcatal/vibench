import os
from messaging_client import get_translation_client
from messaging_models import EventMessage, TranslatedMessage
import json


def translate_message_payload(
    message: EventMessage, target_language_code: str = "es"
) -> TranslatedMessage:
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    # Assuming the text to be translated is within a specific key in message.data
    # For this example, let's assume it's in a "text_to_translate" key.
    # You might need to adjust this based on your actual message structure.
    text_to_translate = message.data.get("text_to_translate", "")

    if not text_to_translate:
        return TranslatedMessage(
            original_text="", translated_text="", target_language=target_language_code
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text_to_translate],
        target_language_code=target_language_code,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text = translation.translated_text
        break  # Take the first translation

    return TranslatedMessage(
        original_text=text_to_translate,
        translated_text=translated_text,
        target_language=target_language_code,
    )


if __name__ == "__main__":
    pass
