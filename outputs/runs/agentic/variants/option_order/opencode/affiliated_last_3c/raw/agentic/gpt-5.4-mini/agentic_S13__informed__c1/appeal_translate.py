from google.cloud import translate_v3 as translate


def appeal_translate(text, target_language_code):
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent="projects/placeholder/locations/global",
    )
    return response.translations[0].translated_text if response.translations else ""
