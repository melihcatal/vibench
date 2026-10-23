from google.cloud import translate_v2 as translate

def create_translate_client():
    return translate.Client()

def translate_text(client, text, target_language):
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def normalize_text(text):
    return text.strip().lower()