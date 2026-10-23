from google.cloud import translate_v2 as translate

def stored_text_translate(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    print('Translated text: {}'.format(result['translatedText']))
    return result['translatedText']