import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

# Google Cloud Translation API Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")


def translate_consent_text(text: str, target_language: str) -> Dict[str, Any]:
    """Translate identity-provider consent copy using Google Cloud Translation API."""
    client = translate.Client(project=GCP_PROJECT_ID)
    result = client.translate(
        text,
        target_language=target_language,
        format_="text",
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "input_text": text,
    }
