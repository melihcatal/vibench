from google.cloud import translate_v2 as translate

def translate_caption(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
