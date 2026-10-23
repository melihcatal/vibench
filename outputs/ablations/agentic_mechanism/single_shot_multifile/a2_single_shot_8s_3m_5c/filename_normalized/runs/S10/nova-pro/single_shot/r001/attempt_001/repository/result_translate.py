from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    client = translate.Client()
    response = client.translate(text, target_language=target_language)
    return response['translatedText']