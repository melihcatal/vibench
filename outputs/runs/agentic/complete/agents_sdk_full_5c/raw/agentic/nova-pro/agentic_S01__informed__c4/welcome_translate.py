from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

translate_client = translate.Client()

def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']