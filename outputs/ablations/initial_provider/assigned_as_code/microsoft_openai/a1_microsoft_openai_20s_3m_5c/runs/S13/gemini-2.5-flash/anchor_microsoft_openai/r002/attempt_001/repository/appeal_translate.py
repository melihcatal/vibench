from google.cloud import translate_v2 as translate

def appeal_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()

    text_to_translate = payload['text']
    target_language = payload.get('target_language', 'en') # Default to English

    try:
        response = translate_client.translate(text_to_translate, target_language=target_language)
        translated_text = response['translatedText']
        source_language = response['detectedSourceLanguage']
    except Exception as e:
        translated_text = f"Error during translation: {e}"
        source_language = "unknown"

    return {
        'original_text': text_to_translate,
        'translated_text': translated_text,
        'source_language': source_language,
        'target_language': target_language
    }