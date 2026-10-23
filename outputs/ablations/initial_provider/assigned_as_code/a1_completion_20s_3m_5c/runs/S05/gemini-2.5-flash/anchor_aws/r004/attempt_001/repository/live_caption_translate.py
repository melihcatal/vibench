from google.cloud import translate_v2 as translate

def live_caption_translate(caption_text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(caption_text, target_language=target_language)
    return result['translatedText']
