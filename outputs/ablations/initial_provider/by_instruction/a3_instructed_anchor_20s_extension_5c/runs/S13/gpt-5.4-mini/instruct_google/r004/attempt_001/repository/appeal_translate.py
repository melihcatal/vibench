from google.cloud import translate_v3 as translate


def appeal_translate(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    return client.translate_text(content=text, target_language_code=target_language, parent="projects/dummy/locations/global").translations[0].translated_text
