from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str, project_id: str):
    # Google Cloud Translation API
    # Provider-identifying signal: google-cloud-translate
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
