from google.cloud import translate_v2 as translate
import os

def translate_script(text: str, target_language: str, project_id: str) -> str:
    client = translate.Client(project=project_id)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate via other means as per Google Cloud docs.

    result = client.translate(text, target_language=target_language)
    return result['translatedText']
