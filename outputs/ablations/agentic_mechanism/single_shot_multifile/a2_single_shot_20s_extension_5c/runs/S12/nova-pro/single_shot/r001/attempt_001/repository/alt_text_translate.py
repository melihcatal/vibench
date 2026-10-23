from google.cloud import translate_v2 as translate

def alt_text_translate(text, target_language='es'):
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']