import os
import json
from typing import Dict, Any
import boto3
from messaging_models import PubsubMessage

def translate_payload_text(message: PubsubMessage, target_language_code: str = "es") -> Dict[str, Any]:
    """Translates customer-facing message payload text using AWS Translate.

    Args:
        message: The PubsubMessage object containing the payload to translate.
        target_language_code: The target language code for translation (e.g., 'es' for Spanish, 'fr' for French).

    Returns:
        A dictionary containing the translated text and translation metadata.
    """
    translate_client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Assuming the text to translate is within the 'data' field of the PubsubMessage
    # and can be directly converted to a string. More complex logic might be needed
    # to identify which specific fields within 'data' are translatable customer-facing text.
    text_to_translate = json.dumps(message.data) if isinstance(message.data, dict) else str(message.data)

    if not text_to_translate.strip():
        return {"translated_text": "", "source_language": "", "target_language": target_language_code, "message": "No text to translate"}

    try:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode="auto", # Automatically detect source language
            TargetLanguageCode=target_language_code
        )
        return response
    except translate_client.exceptions.UnsupportedLanguagePairException as e:
        return {"error": f"Unsupported language pair: {e}"}
    except Exception as e:
        return {"error": f"Translation error: {e}"}

if __name__ == '__main__':
    # Example usage
    customer_message = PubsubMessage(
        message_id="msg-translate-1",
        data={"customer_review": "This product is excellent! I love it."},
        attributes={'context': 'customer_feedback'}
    )

    print("Translating message to Spanish:")
    translated_es = translate_payload_text(customer_message, target_language_code="es")
    print(json.dumps(translated_es, indent=2))

    print("\nTranslating message to French:")
    translated_fr = translate_payload_text(customer_message, target_language_code="fr")
    print(json.dumps(translated_fr, indent=2))

    empty_message = PubsubMessage(
        message_id="msg-empty",
        data={'customer_review': ''},
        attributes={'context': 'customer_feedback'}
    )
    print("\nTranslating empty message:")
    translated_empty = translate_payload_text(empty_message, target_language_code="es")
    print(json.dumps(translated_empty, indent=2))
