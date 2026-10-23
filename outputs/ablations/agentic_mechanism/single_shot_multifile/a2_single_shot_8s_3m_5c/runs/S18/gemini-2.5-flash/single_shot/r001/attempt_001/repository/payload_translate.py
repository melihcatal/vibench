import os
from typing import Dict, Any, Optional
from messaging_client import get_google_translate_client

def translate_message_text(text_content: str, target_language: str = "en") -> Dict[str, Any]:
    translate_client = get_google_translate_client()
    try:
        response = translate_client.translate(
            text_content,
            target_language=target_language
        )
        translated_text = response['translatedText']
        detected_source_language = response.get('detectedSourceLanguage', 'unknown')

        return {
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language
        }
    except Exception as e:
        return {"error": str(e), "translated_text": text_content, "target_language": target_language}