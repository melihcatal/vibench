from google.cloud import translate_v2 as translate

def translate_caption(caption, target_language):
    translation_client = translate.Client()
    translation = translation_client.translate(caption, target_language=target_language)
    translated_caption = translation['translatedText']
    return translated_caption