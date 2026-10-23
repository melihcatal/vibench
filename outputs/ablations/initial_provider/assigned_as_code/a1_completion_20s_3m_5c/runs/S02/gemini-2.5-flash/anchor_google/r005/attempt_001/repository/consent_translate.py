import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language_code: str, source_language_code: str = "en") -> dict:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set in environment variables")

    translate_client = translate.Client(project=project_id)

    # Target can be a language code (e.g. "fr") or a language name (e.g. "French")
    result = translate_client.translate(
        text,
        target_language=target_language_code,
        source_language=source_language_code
    )

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language_code,
    }
