import os
from google.cloud import translate_v2 as translate


def translate_platform_output(
    text: str, target_language: str, project_id: str = None
) -> str:
    translate_client = translate.Client(project=project_id)

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
