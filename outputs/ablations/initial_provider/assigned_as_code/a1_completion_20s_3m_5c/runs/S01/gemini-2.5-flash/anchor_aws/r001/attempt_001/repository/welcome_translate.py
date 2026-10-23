import os

from google.cloud import translate_v2 as translate

from identity_models import ProfileText

def welcome_translate(payload: ProfileText, target_language: str, config: Optional[Dict[str, Any]] = None):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or provide credentials via config.
    
    translate_client = translate.Client()

    text_to_translate = payload.text

    # Translate the text
    # target_language should be an ISO 639-1 code (e.g., 'es' for Spanish, 'fr' for French)
    response = translate_client.translate(text_to_translate, target_language=target_language)
    
    translated_text = response['translatedText']
    source_language = response['detectedSourceLanguage']
    
    return {
        "original_text": text_to_translate,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language
    }
