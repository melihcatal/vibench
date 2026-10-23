from google.cloud import translate_v2 as translate


def translate_text(text, target_language='en'):
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']