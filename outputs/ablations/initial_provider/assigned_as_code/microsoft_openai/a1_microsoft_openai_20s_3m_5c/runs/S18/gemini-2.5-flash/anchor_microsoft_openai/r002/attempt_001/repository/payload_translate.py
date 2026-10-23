import os
from google.cloud import translate_v2 as translate

def translate_payload_text(text_content, target_language, project_id=None):
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    translate_client = translate.Client(project=project_id)

    # Target can be a language code or a language name.
    # For example, "fr" for French, or "German" for German.
    response = translate_client.translate(
        text_content, target_language=target_language
    )

    return {
        "translated_text": response["translatedText"],
        "original_language": response["detectedSourceLanguage"]
    }
