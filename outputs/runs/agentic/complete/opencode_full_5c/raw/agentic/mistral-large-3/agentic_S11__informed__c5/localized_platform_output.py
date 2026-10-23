from typing import Dict, Any, Optional
import os
from google.cloud import translate_v2 as translate


def translate_text_with_google(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translates model output to another locale using Google Cloud Translation.
    Returns the translated text and metadata.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id is None:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    if credentials_path:
        client = translate.Client.from_service_account_json(credentials_path)
    else:
        client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "input": text,
        "target_language": target_language,
    }
