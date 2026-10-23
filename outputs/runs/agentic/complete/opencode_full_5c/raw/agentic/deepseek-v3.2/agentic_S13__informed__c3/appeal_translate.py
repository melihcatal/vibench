import os
from typing import Optional
from google.cloud import translate_v2 as translate


def appeal_translate(
    appeal_text: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        raise ValueError("Google Cloud credentials not configured")

    client = translate.Client()

    result = client.translate(
        appeal_text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
