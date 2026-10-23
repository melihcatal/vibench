from google.cloud import translate_v2 as translate
import os


def script_translate(payload, config=None):
    config = config or {}
    
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['google_application_credentials_path']
    
    translate_client = translate.Client()
    
    text = payload['text']
    target_language = payload['target_language']
    
    result = translate_client.translate(text, target_language=target_language)
    
    return {'translated_text': result['translatedText'], 'detected_source_language': result['detectedSourceLanguage']}