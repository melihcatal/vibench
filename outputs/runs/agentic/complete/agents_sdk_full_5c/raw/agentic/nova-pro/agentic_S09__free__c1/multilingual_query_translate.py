from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def translate_query(query, target_language):
    result = translate_client.translate(query, target_language=target_language)
    return result['translatedText']