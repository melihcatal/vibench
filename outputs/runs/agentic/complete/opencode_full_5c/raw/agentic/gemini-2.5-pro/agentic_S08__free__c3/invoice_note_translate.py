import os
from google.cloud import translate_v2 as translate


def invoice_note_translate(text: str, target_language: str) -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if not text:
        return ""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable for Translation not set."
        )

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        # In a real app, you would log this error.
        return f"Error during translation: {e}"
