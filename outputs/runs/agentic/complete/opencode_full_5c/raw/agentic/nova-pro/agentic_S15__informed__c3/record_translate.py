from google.cloud import translate


def record_translate(text, target_language):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/-/locations/{location}"
    response = client.translate_text(
        parent=parent, contents=[text], target_language_code=target_language
    )
    return [translation.translated_text for translation in response.translations]
