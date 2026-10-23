from google.cloud import translate_v2 as translate

def translate_caption(caption, target_language):
    client = translate.Client()
    result = client.translate(caption, target_language=target_language)
    return result['translatedText']