import google.cloud.translate as translate

def translate_text(text, target_language='en'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']