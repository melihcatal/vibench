from google.cloud import translate_v2 as translate

def translate_payload(payload, target_language='en'):
    translation_client = translate.Client()
    result = translation_client.translate(payload, target_language=target_language)
    return result['translatedText']