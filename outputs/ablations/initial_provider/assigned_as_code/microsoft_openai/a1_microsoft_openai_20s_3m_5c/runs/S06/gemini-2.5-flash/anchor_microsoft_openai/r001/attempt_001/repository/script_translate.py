from google.cloud import translate_v2 as translate
import os

def translate_script(text, target_language, project_id=None):
    if not project_id:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    
    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
    }