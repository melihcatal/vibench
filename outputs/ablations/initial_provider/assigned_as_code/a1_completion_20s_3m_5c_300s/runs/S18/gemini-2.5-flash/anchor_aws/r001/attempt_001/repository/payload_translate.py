import os
from typing import Dict, Any

import boto3

from messaging_models import Message

def translate_payload_text(message: Message, region_name: str, target_language_code: str = 'es') -> Dict[str, Any]:
    """
    Translates customer-facing message payload text using AWS Translate.
    Assumes the original text is in English unless otherwise specified.
    """
    translate_client = boto3.client("translate", region_name=region_name)

    translation_results = {
        "message_id": message.id,
        "original_text": None,
        "translated_text": None,
        "source_language": None,
        "target_language": target_language_code,
        "status": "no_text_to_translate"
    }

    # Assuming the text to translate is in message.body["customer_facing_text"]
    text_to_translate = message.body.get("customer_facing_text")

    if text_to_translate and isinstance(text_to_translate, str):
        try:
            # Detect dominant language first if not known, or assume 'en'
            # For simplicity, assuming source is 'auto' to let AWS detect, or 'en' if no auto-detection is available for a specific operation.
            # AWS Translate can detect source language automatically.
            response = translate_client.translate_text(
                Text=text_to_translate,
                SourceLanguageCode='auto',
                TargetLanguageCode=target_language_code
            )
            translation_results["original_text"] = text_to_translate
            translation_results["translated_text"] = response["TranslatedText"]
            translation_results["source_language"] = response["SourceLanguageCode"]
            translation_results["status"] = "translated"
        except Exception as e:
            translation_results["status"] = "error"
            translation_results["details"] = str(e)
    
    return translation_results
