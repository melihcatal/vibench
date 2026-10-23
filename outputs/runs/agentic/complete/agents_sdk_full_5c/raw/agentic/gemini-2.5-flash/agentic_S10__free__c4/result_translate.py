from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, target_language: str, project_id: str = None) -> str:
    """Translates generated model output using Google Cloud Translation API."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    client = translate.TranslationServiceClient()
    
    parent = f"projects/{project_id}/locations/global"
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )
    
    # The response can contain multiple translations, we take the first one.
    if response.translations:
        return response.translations[0].translated_text
    return ""
