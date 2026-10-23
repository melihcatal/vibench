from google.cloud import translate_v2 as translate

def appeal_translate(text, target_language='es'):
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']