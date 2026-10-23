from google.cloud import translate_v2 as translate

def alt_text_translate(text, target_language, config=None):
    config = config or {}
    translate_client = translate.Client(credentials=config.get('google_credentials'))

    if isinstance(text, bytes):
        text = text.decode('utf-8')

    result = translate_client.translate(text, target_language=target_language)
    return {'translated_text': result['translatedText'], 'detected_source_language': result['detectedSourceLanguage']}
