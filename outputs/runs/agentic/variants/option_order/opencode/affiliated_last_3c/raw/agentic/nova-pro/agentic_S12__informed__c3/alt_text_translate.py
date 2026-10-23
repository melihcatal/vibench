import google.cloud.translate as translate


def alt_text_translate(text, target_language):
    client = translate.TranslationServiceClient()
    response = client.translate_text(text=text, target_language_code=target_language)
    return response.translations[0].translated_text
