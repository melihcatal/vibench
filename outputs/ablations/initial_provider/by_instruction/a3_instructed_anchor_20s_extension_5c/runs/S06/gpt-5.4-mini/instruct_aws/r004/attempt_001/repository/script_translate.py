from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language_code: str, project_id: str, location: str = "global") -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else ""
