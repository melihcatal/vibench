from google.cloud import translate_v3 as translate


def alt_text_translate(text: str, target_language: str):
    client = translate.TranslationServiceClient()
    parent = client.location_path("project", "global")
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else ""
