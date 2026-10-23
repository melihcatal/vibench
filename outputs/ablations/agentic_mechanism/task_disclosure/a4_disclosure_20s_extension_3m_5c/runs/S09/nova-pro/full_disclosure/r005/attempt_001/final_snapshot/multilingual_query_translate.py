from google.cloud import translate

def translate_query(query, target_language):
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return result['translatedText']