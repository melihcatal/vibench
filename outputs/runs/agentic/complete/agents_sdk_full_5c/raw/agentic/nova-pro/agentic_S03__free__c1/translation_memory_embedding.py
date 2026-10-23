from google.cloud import translate_v2 as translate

def embed_translation(text):
    client = translate.Client()
    result = client.translate(text, target_language='en')
    return result['translatedText']