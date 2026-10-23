from google.cloud import translate_v2 as translate
import os

def translate_script(text: str, target_language: str) -> str:
    client = translate.Client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    response = client.translate(text, target_language=target_language, project_id=project_id)
    return response["translatedText"]
