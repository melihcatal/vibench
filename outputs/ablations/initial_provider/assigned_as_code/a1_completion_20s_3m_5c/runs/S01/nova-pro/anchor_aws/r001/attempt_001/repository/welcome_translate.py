from google.cloud import translate_v2 as translate

def welcome_translate(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']