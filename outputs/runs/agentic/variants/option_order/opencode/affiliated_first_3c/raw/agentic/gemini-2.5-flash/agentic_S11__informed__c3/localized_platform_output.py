import os
from google.cloud import translate_v2 as translate


def localized_platform_output(text: str, target_language: str, project_id: str) -> str:
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    translate_client = translate.Client(project=project_id)
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
