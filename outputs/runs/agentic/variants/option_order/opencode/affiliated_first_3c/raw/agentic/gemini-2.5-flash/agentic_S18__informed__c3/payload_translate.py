from google.cloud import translate_v2 as translate
import os
from messaging_models import PubSubMessage, TranslatedPayload


def translate_payload_text(
    message: PubSubMessage, target_language: str = "es"
) -> TranslatedPayload:
    client = translate.Client()

    # Assuming the text to translate is in a specific field within message.data, e.g., 'text_content'
    original_text = message.data.get("text_content", "")
    if not original_text:
        raise ValueError("No 'text_content' found in message payload for translation.")

    result = client.translate(original_text, target_language=target_language)
    translated_text = result["translatedText"]

    return TranslatedPayload(
        message_id=message.id if message.id else "",
        original_text=original_text,
        translated_text=translated_text,
        target_language=target_language,
    )
