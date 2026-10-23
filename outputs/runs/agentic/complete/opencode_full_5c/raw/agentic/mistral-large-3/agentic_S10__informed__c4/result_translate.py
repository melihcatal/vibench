import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def result_translate(
    text: str,
    target_language: str = "es",
    source_language: str = None,
    project_id: str = None,
) -> str:
    """
    Translates generated model output using Google Cloud Translation.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., "es" for Spanish).
        source_language: Source language code (e.g., "en" for English). If None, auto-detects.
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT environment variable.

    Returns:
        Translated text.
    """
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = translate.Client(project=project_id)

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
