from observability_client import get_cloudwatch_translate_client
from typing import List, Dict
import os

def translate_log_messages(log_messages: List[str], target_language_code: str = "es", source_language_code: str = "en") -> Dict[str, str]:
    client = get_cloudwatch_translate_client()
    
    translated_messages = {}
    for i, message in enumerate(log_messages):
        if not message.strip():
            translated_messages[f"log_message_{i}"] = ""
            continue

        try:
            response = client.translate_text(
                Text=message,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code
            )
            translated_messages[f"log_message_{i}"] = response["TranslatedText"]
        except Exception as e:
            print(f"Error translating log message {i}: {e}")
            translated_messages[f"log_message_{i}"] = f"Translation_Error: {e}"
    return translated_messages
