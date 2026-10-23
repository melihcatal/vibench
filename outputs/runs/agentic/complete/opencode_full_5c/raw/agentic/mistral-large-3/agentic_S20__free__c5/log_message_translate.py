from typing import List
from google.cloud import translate_v2 as translate


def translate_log_messages(
    log_messages: List[str], target_language: str = "es"
) -> List[dict]:
    """Translate log messages to another locale using Google Cloud Translation."""
    translate_client = translate.Client()

    results = []
    for message in log_messages:
        result = translate_client.translate(message, target_language=target_language)

        results.append(
            {
                "original_message": message,
                "translated_message": result["translatedText"],
                "detected_source_language": result["detectedSourceLanguage"],
            }
        )

    return results
