from google.cloud import translate

def translate_output(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/-/locations/global"
    response = client.translate_text(parent=parent, contents=[text], mime_type="text/plain", target_language_code=target_language)
    return response.translations[0].translated_text
