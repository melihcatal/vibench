from google.cloud import translate_v3


def translate_script(text: str, target_language: str, project_id: str, location: str = "global") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    return response.translations[0].translated_text
