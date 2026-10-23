from google.cloud import translate


def translate_platform_output(text, target_language):
    client = translate.TranslationServiceClient()
    response = client.translate_text(text, target_language=target_language)
    return response.translations[0].translated_text
