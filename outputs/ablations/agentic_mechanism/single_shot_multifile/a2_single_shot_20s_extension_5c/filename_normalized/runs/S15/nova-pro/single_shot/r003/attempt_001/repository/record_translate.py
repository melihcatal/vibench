from google.cloud import translate_v2 as translate

def translate_record(record, target_language='en'):
    translate_client = translate.Client()
    translation = translate_client.translate(record['content'], target_language=target_language)
    return {'translated_content': translation['translatedText']}