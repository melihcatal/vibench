from google.cloud import translate_v2 as translate
import os
from typing import Optional


def log_message_translate(text: str, target_language: str = "fr") -> Optional[str]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
