import os
import google.cloud.translate_v2 as translate

def translate_description(english_description, target_lang='es'):
    """
    Translate a short visual description to the target language using Google Cloud Translation.
    Returns the translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(english_description, target_language=target_lang)
    return result['translatedText']
