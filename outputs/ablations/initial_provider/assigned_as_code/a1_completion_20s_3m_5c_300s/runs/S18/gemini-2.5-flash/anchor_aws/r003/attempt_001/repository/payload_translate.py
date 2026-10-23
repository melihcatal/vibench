import os
import boto3

from messaging_models import Message

def translate_payload_text(message: Message, target_language_code: str, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    source_language_code = config.get("source_language_code", "auto") # 'auto' for automatic detection

    translate_client = boto3.client("translate", region_name=region_name)

    text_to_translate = str(message.payload) # Convert payload to string for translation

    response = translate_client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    translated_text = response['TranslatedText']
    source_language_detected = response['SourceLanguageCode']

    # Update message payload with translated text or return it separately
    # For this example, we'll return the translated text and not modify the original message object.

    return {
        "message_id": message.message_id,
        "original_payload": message.payload,
        "translated_text": translated_text,
        "source_language_detected": source_language_detected,
        "target_language": target_language_code
    }
