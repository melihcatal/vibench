from google.cloud import translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def translate_consent(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/-/locations/global"
    response = client.translate_text(
        parent, text, target_language, mime_type="text/plain"
    )
    return response.translations[0].translated_text
