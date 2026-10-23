from google.cloud import translate_v3 as translate


def translate_ocr_text(
    text: str, project_id: str, target_language: str, location: str = "global"
) -> str:
    client = translate.TranslationServiceClient()
    parent = client.location_path(project_id, location)
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else ""
