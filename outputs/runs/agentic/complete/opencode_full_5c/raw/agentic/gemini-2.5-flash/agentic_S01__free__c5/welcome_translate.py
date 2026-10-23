from google.cloud import translate_v2 as translate
import os


def welcome_translate(text: str, target_language: str) -> str:
    translate_client = translate.Client()
    # Project ID is usually picked up from GOOGLE_APPLICATION_CREDENTIALS or environment variables
    # For explicit setting: project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
