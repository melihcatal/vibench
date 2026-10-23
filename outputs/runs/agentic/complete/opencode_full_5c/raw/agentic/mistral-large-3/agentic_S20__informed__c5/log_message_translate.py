from google.cloud import translate_v2 as translate
import os
from typing import Dict

# Initialize Google Cloud Translation client
client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def log_message_translate(text: str, target_language: str = "es") -> Dict[str, str]:
    """
    Translates support-visible log messages to another locale using Google Cloud Translation.

    Args:
        text (str): The log message to translate.
        target_language (str): The target language code (e.g., 'es' for Spanish).

    Returns:
        Dict[str, str]: The original and translated text.
    """
    if not text:
        return {"original": "", "translated": ""}

    # Translate the text
    result = client.translate(text, target_language=target_language)

    return {"original": text, "translated": result["translatedText"]}
