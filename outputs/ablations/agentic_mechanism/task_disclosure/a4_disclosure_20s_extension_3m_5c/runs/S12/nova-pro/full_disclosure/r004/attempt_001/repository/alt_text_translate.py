from google.cloud import translate_v2 as translate

def translate_description(description, target_language):
    client = translate.Client()
    result = client.translate(description, target_language=target_language)
    return result['translatedText']