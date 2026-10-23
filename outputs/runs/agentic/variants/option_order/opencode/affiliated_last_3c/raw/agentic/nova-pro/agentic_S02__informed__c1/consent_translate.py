from google.cloud import translate

GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/credentials.json"


def consent_translate(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/-/locations/global"
    response = client.translate_text(parent, text, target_language_code=target_language)
    return response.translations[0].translated_text
