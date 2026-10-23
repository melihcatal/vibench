from google.cloud import translate


def batch_translate(texts, target_lang):
    client = translate.TranslationServiceClient()
    parent = client.location_path("your-project-id", "global")
    response = client.translate_text(parent, texts, target_language_code=target_lang)
    return [translation.translated_text for translation in response.translations]
