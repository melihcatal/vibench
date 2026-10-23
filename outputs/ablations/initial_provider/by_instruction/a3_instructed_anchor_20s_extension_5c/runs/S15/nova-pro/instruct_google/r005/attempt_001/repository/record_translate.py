from google.cloud import translate

def translate_text(text, target_language='en'):
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']