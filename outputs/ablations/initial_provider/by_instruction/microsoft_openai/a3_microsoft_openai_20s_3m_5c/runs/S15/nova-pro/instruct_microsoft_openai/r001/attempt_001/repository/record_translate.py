from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

def record_translate(endpoint, key, text, to_language):
    translation_client = TextTranslationClient(endpoint=endpoint, credential=TextTranslationApiKeyCredential(key))
    result = translation_client.translate([text], to_language)[0]
    return result.translations[0].text