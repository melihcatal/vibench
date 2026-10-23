from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def stored_text_translate(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']