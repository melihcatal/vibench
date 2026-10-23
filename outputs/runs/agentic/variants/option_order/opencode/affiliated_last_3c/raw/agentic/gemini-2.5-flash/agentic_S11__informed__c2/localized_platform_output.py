import os
from google.cloud import translate_v2 as translate


def translate_output(text: str, target_language: str, project_id: str) -> dict:
    """
    Translates platform model output for another locale using Google Cloud Translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set."
        )

    translate_client = translate.Client(project=project_id)

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
