from google.cloud import translate

def translate_query(query, target_language):
    client = translate.TranslateClient()
    translation = client.translate(query, target_language=target_language)
    return translation['translatedText']