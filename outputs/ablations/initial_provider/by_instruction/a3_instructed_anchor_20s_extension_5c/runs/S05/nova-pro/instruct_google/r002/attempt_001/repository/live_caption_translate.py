from google.cloud import translate

# Translate live captions into another language
def live_caption_translate(text, target_language='es'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']