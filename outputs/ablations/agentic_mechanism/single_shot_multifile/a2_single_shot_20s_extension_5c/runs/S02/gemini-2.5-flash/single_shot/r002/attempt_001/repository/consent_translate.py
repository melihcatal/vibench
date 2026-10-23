import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    try:
        translate_client = translate.Client(project=project_id)

        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "original_text": result["input"]
        }
    except Exception as e:
        raise RuntimeError(f"Failed to translate consent copy with Google Cloud Translation: {e}")