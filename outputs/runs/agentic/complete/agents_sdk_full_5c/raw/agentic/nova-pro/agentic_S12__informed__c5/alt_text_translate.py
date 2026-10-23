from google.cloud import translate_v2 as translate

def translate_alt_text(alt_text, target_language):
    translation_client = translate.Client()
    translation = translation_client.translate(alt_text, target_language=target_language)
    return translation['translatedText']