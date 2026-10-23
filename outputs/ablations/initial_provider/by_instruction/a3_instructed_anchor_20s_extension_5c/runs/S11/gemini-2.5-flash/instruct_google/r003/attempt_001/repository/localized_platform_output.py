from google.cloud import translate_v3 as translate

def translate_google_output(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates platform model output using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    
    # The concrete provider (Google Cloud Translation API) is identified by the import
    # and the specific API endpoint used for translation.
    
    parent = f"projects/{project_id}/locations/global"
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )
    
    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
        
    return translated_text
